import "server-only";
import { and, count, eq, isNull, sql } from "drizzle-orm";
import { db } from "@/db";
import { friendInvites, friendships, profiles } from "@/db/schema";
import { sendEmailBestEffort } from "@/lib/email";
import { friendInviteEmail } from "@/lib/email/templates";
import type { Db } from "@/lib/tracker/service";
import { normalizeInviteEmail } from "./invite-email";
import { collectFriendIds, orderedPair } from "./pairs";

// Friends service. Mirrors Curfew's inviteToGroup logic, retargeted from a
// group to a pair. The invite row IS the request; the email is a nudge.

/** Maximum pending invites a single sender may have at once. */
export const INVITE_CAP = 20;

// ---------------------------------------------------------------------------
// Reads
// ---------------------------------------------------------------------------

export type PendingInvite = {
  id: string;
  inviterName: string;
  createdAt: string;
};

/**
 * Pending invites addressed to this email that the recipient has not dismissed.
 * This is what their dashboard lists.
 */
export async function pendingFor(email: string, q: Db = db): Promise<PendingInvite[]> {
  const rows = await q
    .select({
      id: friendInvites.id,
      inviterName: profiles.name,
      createdAt: friendInvites.createdAt,
    })
    .from(friendInvites)
    .innerJoin(profiles, eq(profiles.userId, friendInvites.invitedBy))
    .where(and(eq(friendInvites.email, email.toLowerCase()), eq(friendInvites.status, "pending"), isNull(friendInvites.dismissedAt)))
    .orderBy(friendInvites.createdAt);
  return rows;
}

export type SentInvite = {
  id: string;
  email: string;
  status: string;
  createdAt: string;
  respondedAt: string | null;
};

/** Invites the viewer has sent, newest first. */
export async function sentBy(inviterId: string, q: Db = db): Promise<SentInvite[]> {
  return q
    .select({
      id: friendInvites.id,
      email: friendInvites.email,
      status: friendInvites.status,
      createdAt: friendInvites.createdAt,
      respondedAt: friendInvites.respondedAt,
    })
    .from(friendInvites)
    .where(eq(friendInvites.invitedBy, inviterId))
    .orderBy(sql`${friendInvites.createdAt} desc`);
}

/**
 * Returns all user ids that the viewer can see on the scoreboard, including
 * the viewer themselves. Callers replace `innerJoin(userApprovals…)` with
 * `inArray(x.userId, ids)` — the viewer is included so no extra `or
 * user_id = viewerId` clause is needed.
 */
export async function friendIds(viewerId: string, q: Db = db): Promise<string[]> {
  const rows = await q
    .select({ userA: friendships.userA, userB: friendships.userB })
    .from(friendships)
    .where(sql`${friendships.userA} = ${viewerId} or ${friendships.userB} = ${viewerId}`);
  return collectFriendIds(viewerId, rows);
}

/** The viewer's friends, excluding the viewer — the people whose activity you see. */
export async function otherFriendIds(viewerId: string, q: Db = db): Promise<string[]> {
  return (await friendIds(viewerId, q)).filter((id) => id !== viewerId);
}

/** True if the two users are already friends (order-independent). */
async function areFriends(a: string, b: string, q: Db = db): Promise<boolean> {
  const [lo, hi] = orderedPair(a, b);
  const [row] = await q
    .select({ n: count() })
    .from(friendships)
    .where(and(eq(friendships.userA, lo), eq(friendships.userB, hi)));
  return (row?.n ?? 0) > 0;
}

// ---------------------------------------------------------------------------
// Mutations
// ---------------------------------------------------------------------------

/**
 * Send a friend invite. Guards the two nonsense cases (self, already friends).
 * A repeat invite is a silent no-op (the unique index handles it).
 * Caps at INVITE_CAP pending invites per sender.
 */
export async function invite(inviterId: string, rawEmail: string, q: Db = db): Promise<void> {
  const email = normalizeInviteEmail(rawEmail);

  // If the address already has an account, guard the two nonsense cases.
  const [existing] = await q.execute(sql`select id from auth.users where lower(email) = ${email}`);
  if (existing) {
    const row = existing as { id: string };
    if (row.id === inviterId) throw new Error("You cannot invite yourself.");
    if (await areFriends(inviterId, row.id, q)) throw new Error("You are already friends.");
  }

  // Cap pending invites per sender.
  const [capRow] = await q
    .select({ n: count() })
    .from(friendInvites)
    .where(and(eq(friendInvites.invitedBy, inviterId), eq(friendInvites.status, "pending")));
  if ((capRow?.n ?? 0) >= INVITE_CAP) {
    throw new Error(`You have ${INVITE_CAP} pending invites. Revoke one before sending another.`);
  }

  const [row] = await q
    .insert(friendInvites)
    .values({ email, invitedBy: inviterId })
    .onConflictDoNothing()
    .returning({ id: friendInvites.id });
  if (!row) return; // Already invited: silent no-op.

  const [me] = await q.select({ name: profiles.name }).from(profiles).where(eq(profiles.userId, inviterId));
  await sendEmailBestEffort({
    actorId: inviterId,
    kind: "invite",
    email: friendInviteEmail(email, me?.name ?? "Someone"),
    payload: { invite_id: row.id },
  });
}

/** Loads an invite by id, or throws. Shared so every mutation reports the same
 * "not found" and "no longer pending" reasons. */
async function requirePendingInvite(inviteId: string, q: Db) {
  const [inv] = await q.select().from(friendInvites).where(eq(friendInvites.id, inviteId));
  if (!inv) throw new Error("Invite not found.");
  if (inv.status !== "pending") throw new Error("Invite is no longer pending.");
  return inv;
}

/**
 * Accept a pending invite. The invite id selects which of the invites
 * addressed to *your* email you are acting on — a leaked link is useless to
 * anyone who does not own that address.
 */
export async function accept(inviteId: string, userId: string, userEmail: string, q: Db = db): Promise<void> {
  await q.transaction(async (tx) => {
    const inv = await requirePendingInvite(inviteId, tx);
    if (inv.email.toLowerCase() !== userEmail.toLowerCase()) throw new Error("Invite is for a different email.");
    await tx.update(friendInvites).set({ status: "accepted", respondedAt: new Date().toISOString() }).where(eq(friendInvites.id, inviteId));
    const [lo, hi] = orderedPair(inv.invitedBy, userId);
    await tx.insert(friendships).values({ userA: lo, userB: hi, fromInvite: inviteId }).onConflictDoNothing();
  });
}

/**
 * Refuse a pending invite. Sets status to 'revoked' so the sender can see it.
 */
export async function refuse(inviteId: string, userEmail: string, q: Db = db): Promise<void> {
  const inv = await requirePendingInvite(inviteId, q);
  if (inv.email.toLowerCase() !== userEmail.toLowerCase()) throw new Error("Invite is for a different email.");
  await q.update(friendInvites).set({ status: "revoked", respondedAt: new Date().toISOString() }).where(eq(friendInvites.id, inviteId));
}

/**
 * Dismiss a pending invite. Status stays 'pending'; dismissed_at is stamped.
 * The sender sees no change; the invite stops being listed for the recipient.
 * Someone who dismisses has decided only that they do not want to look at it.
 */
export async function dismiss(inviteId: string, userEmail: string, q: Db = db): Promise<void> {
  const inv = await requirePendingInvite(inviteId, q);
  if (inv.email.toLowerCase() !== userEmail.toLowerCase()) throw new Error("Invite is for a different email.");
  await q.update(friendInvites).set({ dismissedAt: new Date().toISOString() }).where(eq(friendInvites.id, inviteId));
}

/**
 * Revoke an invite the viewer sent. Sets status to 'revoked'.
 */
export async function revoke(inviteId: string, inviterId: string, q: Db = db): Promise<void> {
  const inv = await requirePendingInvite(inviteId, q);
  if (inv.invitedBy !== inviterId) throw new Error("That is not your invite.");
  await q.update(friendInvites).set({ status: "revoked", respondedAt: new Date().toISOString() }).where(eq(friendInvites.id, inviteId));
}

/**
 * Unfriend: delete the pair row. A friend graph with no exit is a trap.
 */
export async function unfriend(viewerId: string, otherId: string, q: Db = db): Promise<void> {
  const [lo, hi] = orderedPair(viewerId, otherId);
  await q.delete(friendships).where(and(eq(friendships.userA, lo), eq(friendships.userB, hi)));
}
