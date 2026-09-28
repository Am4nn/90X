import "server-only";
import { key } from "@/lib/upstash/keys";
import { redis } from "@/lib/upstash/redis";

// Telling "I pressed Stop" apart from "I closed the app".
//
// At the HTTP level they are the same event: the client stops reading and the
// request aborts. But they mean opposite things. Closing the app should leave the
// answer to finish and be waiting on return; pressing Stop should stop the model
// immediately, because the reader has said they do not want it and every further
// token is billed for nothing.
//
// So generation no longer follows the connection, and Stop says so out of band:
// the client posts here, this leaves a flag, and the run checks for it between
// polls and aborts. Redis rather than memory because the flag has to reach
// whichever instance is running the reply, which is not necessarily the one that
// takes the stop request.

/** Long enough to outlive the slowest reply, short enough to forget. */
const TTL_SECONDS = 360;
const POLL_MS = 1500;

const stopKey = (userId: string, threadId: string) => key("coach", "stop", userId, threadId);

/** The reader pressed Stop. */
export async function requestStop(userId: string, threadId: string): Promise<void> {
  await redis().set(stopKey(userId, threadId), "1", { ex: TTL_SECONDS });
}

/** Cleared when a run starts, so a stop from a previous reply cannot kill this one. */
export async function clearStop(userId: string, threadId: string): Promise<void> {
  await redis().del(stopKey(userId, threadId));
}

/**
 * Aborts the returned signal when a stop arrives for this thread.
 *
 * Polling, because Redis has no push we can wait on here and a reply is short
 * lived: one GET every 1.5 seconds for the life of an answer. `done()` stops the
 * polling and must be called whether the run finished or threw, or the interval
 * outlives the request.
 */
export function stopSignal(userId: string, threadId: string): { signal: AbortSignal; done: () => void } {
  const controller = new AbortController();
  const timer = setInterval(async () => {
    try {
      if (await redis().get(stopKey(userId, threadId))) {
        controller.abort(new Error("the reader pressed Stop"));
        clearInterval(timer);
        await clearStop(userId, threadId);
      }
    } catch {
      // A Redis blip must not abort a reply that is going fine.
    }
  }, POLL_MS);
  // Node keeps the process alive for a pending interval; this one is bookkeeping.
  timer.unref?.();
  return { signal: controller.signal, done: () => clearInterval(timer) };
}
