"use client";

import { useEffect, useRef } from "react";
import { markStudiedAction } from "@/app/actions/today";
import { dwellMs } from "@/lib/library/dwell";

// Reading a lesson marks the topic studied, but only on evidence (decision
// 2026-09-28). Two conditions, both required:
//
//   - the end of the lesson has been on screen, so it was scrolled through
//   - a minimum time has passed, scaled to the lesson's length
//
// Scrolling alone is a keystroke. "Studied" feeds coverage in the readiness
// score, so a glance that moves that number makes the score a lie. The manual
// button stays: it is how you say "I knew this already" without the wait.

export function AutoStudied({ slug, words, studied }: { slug: string; words: number; studied: boolean }) {
  const endRef = useRef<HTMLDivElement>(null);
  const sent = useRef(false);

  useEffect(() => {
    if (studied || sent.current) return;
    const end = endRef.current;
    if (!end || typeof IntersectionObserver === "undefined") return;

    const opened = Date.now();
    const needed = dwellMs(words);
    let timer: ReturnType<typeof setTimeout> | undefined;

    const mark = () => {
      if (sent.current) return;
      sent.current = true;
      // Failure is silent on purpose: the manual button is right there, and an
      // error toast for something the reader never asked for is noise.
      void markStudiedAction(slug, true);
    };

    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((e) => e.isIntersecting)) return;
      const waited = Date.now() - opened;
      if (waited >= needed) mark();
      else if (timer === undefined) timer = setTimeout(mark, needed - waited);
    });
    observer.observe(end);

    return () => {
      observer.disconnect();
      if (timer !== undefined) clearTimeout(timer);
    };
  }, [slug, words, studied]);

  return <div ref={endRef} aria-hidden="true" />;
}
