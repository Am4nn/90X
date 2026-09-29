import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { Logo } from "@/components/brand";
import { CoachIcon, FeedIcon, FriendsIcon, LibraryIcon, MeIcon, TodayIcon } from "@/components/icons";
import { requireViewer } from "@/lib/auth/viewer";
import { createClient } from "@/lib/supabase/server";
import { SetupForm } from "./setup-form";

export const metadata: Metadata = { title: "Set up" };

// The desktop shell for onboarding: the six app sections with Set up active
// (mock §onboarding). Set up itself is not a link — you are already on it.
const SHELL = [
  { href: "/today", label: "Today", Icon: TodayIcon },
  { href: "/feed", label: "Feed", Icon: FeedIcon },
  { href: "/library", label: "Library", Icon: LibraryIcon },
  { href: "/coach", label: "Coach", Icon: CoachIcon },
  { href: "/friends", label: "Friends", Icon: FriendsIcon },
  { href: "/me", label: "Me", Icon: MeIcon },
] as const;

export default async function SetupPage() {
  const viewer = await requireViewer({ allowSetup: true });
  if (viewer.setupDone) redirect("/today");
  const supabase = await createClient();
  // `name` is one of the three columns the authenticated role can still read;
  // `timezone` is not, and it isn't used here anyway.
  const { data: profile } = await supabase.from("profiles").select("name").eq("user_id", viewer.id).single();
  return (
    <div className="flex min-h-dvh">
      <aside className="sticky top-0 hidden h-dvh w-[220px] shrink-0 flex-col gap-1.5 border-r border-line px-3.5 py-6 md:flex">
        <Link href="/today" prefetch={false} className="px-2.5 pb-5">
          <Logo />
        </Link>
        <span aria-current="page" className="flex items-center gap-3 rounded-lg bg-cyan-bg p-2.5 text-body font-semibold text-cyan">
          <span aria-hidden className="size-5" />
          Set up
        </span>
        {SHELL.map(({ href, label, Icon }) => (
          <Link
            key={href}
            href={href}
            prefetch={false}
            className="group flex items-center gap-3 rounded-lg p-2.5 text-body font-semibold text-text-2 transition-colors hover:bg-surface hover:text-text"
          >
            <Icon className="size-5 text-mute group-hover:text-text-2" />
            {label}
          </Link>
        ))}
      </aside>
      <main className="pt-safe-lg mx-auto flex w-full max-w-md flex-1 flex-col px-5 pb-12 md:mx-0 md:max-w-2xl md:px-10 md:pt-8 md:pb-12">
        <SetupForm defaults={{ name: profile?.name || viewer.name, timezone: "" }} />
      </main>
    </div>
  );
}
