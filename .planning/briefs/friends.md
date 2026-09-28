# Brief — Friends: a real friend graph, invites by email

**Read `.planning/briefs/README.md` first.** This brief adds only what is specific to this task.

Branch: your pinned branch. PR to `main`. Land it **after** the `source-grounding` PR merges.

## Why

Today every approved user sees every other approved user. `lib/tracker/me.ts:42`
says it outright — *"You and every approved friend"* — and the query is
`profiles innerJoin user_approvals where status = 'approved'`. There is no friend
graph. One list, everybody on it.

The owner wants: you invite someone by email, they accept or decline, and only
then can the two of you see each other. Nobody can discover who else uses the
app.

Three things already leak more than the scoreboard intends, and this task fixes
them on the way through:

1. `profiles_read` (`supabase/migrations/20260926000001_access.sql:92`) returns
   the **whole profile row** to any approved user — `leetcode_username`,
   `notifications` (their push preferences), `campaign_days`, `timezone`,
   `role`, `language`. Only `name` and `avatar_url` are ever rendered for
   somebody else.
2. `notifyFriends` (`lib/push.ts:65`) pushes every check-in to **every** approved
   user who opted in. It is a broadcast, not a friend notification.
3. `friendActivity` (`lib/tracker/me.ts:95`) returns `profiles.name` **unsplit**,
   so the activity list shows full names while the scoreboard beside it shows
   first names only. `problemDetail`'s `friends` list
   (`lib/library/queries.ts:126`) does the same.

## Copy Curfew

Our sibling project Curfew already ships this flow, and it has been used. You
cannot read that repo, so its design is written out below — **follow it**. Where
this brief and your instincts differ, the brief wins; these choices were made
against a running app.

### The one thing to get right: the invite is bound to the email, not the link

Curfew's invite row id is the only token, and it is **not** a bearer token. The
join screen does this:

```ts
const invites = await listInvitesForEmail(user.email);   // the SESSION user's email
const invite = invites.find((i) => i.id === inviteId);
if (!invite) notFound();
```

So the id in the URL only selects *which* of the invites addressed to your own
signed-in address you are acting on. A leaked link is useless to anybody else.
Every mutation re-checks it:

```ts
if (inv.email.toLowerCase() !== userEmail.toLowerCase()) {
  throw new Error("invite is for a different email");
}
```

**Do not replace this with a random token that anyone holding the URL can
redeem.** The cost of Curfew's choice is that the invitee must sign in with the
address they were invited at; for an app with a handful of users that is the
right trade, and it removes a whole class of leaked-link bugs.

### The email links to the dashboard, not to the invite

Curfew's invite email body is, verbatim in substance:

> *{inviter} invited you to {group} on Curfew.*
> **[Open Curfew]**
> *Sign in with Google. Once your account is approved, accept the invite from your dashboard.*

The button goes to `/`, not to `/join/<id>`. That is deliberate and it is what
makes the already-registered case work: a signed-in user sees the request on
their dashboard without ever opening the email. The email is a nudge; the
**pending invite row is the mechanism**.

### Admin approval stays in the loop

The owner chose this explicitly: an invite does **not** grant app access. An
invited person signs in, lands on `/pending` like anybody else, and only sees
the friend request once an admin approves them. Curfew works the same way — note
the email copy above says so.

Consequence you must handle: approval is currently **silent** in 90x, and with
approval now standing between an invite and its acceptance, that silence is the
bottleneck. Port Curfew's `approvalEmail` too (below).

### Three controls on an invite, not two

Curfew gives the recipient three, and the third is the one people miss:

| Control | Effect |
|---|---|
| **Accept** | Friendship created. |
| **Refuse** | Invite set to `revoked`, `responded_at` stamped. **The sender can see that.** |
| **Dismiss** | Invite stays `pending`, `dismissed_at` stamped. The sender sees **no change**, a link already in hand still works, it just stops being listed. |

Its own comment: *"Someone who dismisses has decided only that they do not want
to look at it."* Build all three.

### Email delivery is best-effort and never fails the action

Curfew's `src/server/email.ts`:

```ts
// Email delivery is a side effect. A delivery failure never changes the result
// of the committed invite, approval, or account-removal action.
export async function sendEmailBestEffort(input: BestEffortEmail): Promise<void> {
  try {
    const emailId = await sendEmail(input.email);
    try { await recordEvent({ ..., type: `email.${input.kind}.sent`, payload: { ..., email_id: emailId } }); }
    catch { /* action committed, email sent; don't surface a log failure */ }
  } catch (error) {
    try { await recordEvent({ ..., type: `email.${input.kind}.failed`, payload: { ..., error: ... } }); }
    catch { /* keep the side effect best-effort even if the failure record can't write */ }
  }
}
```

Port this shape exactly. 90x has no `events` table — use
`lib/activity/service.ts` if it fits, otherwise `console.error` with the invite
id and say so in a comment. The rule that matters: **a Resend outage must not
roll back a committed invite.**

## What exists in 90x

- **Access:** `supabase/migrations/20260926000001_access.sql` — `profiles`,
  `user_approvals`, `is_approved()`, `is_admin()`, the `on_auth_user_created`
  trigger. Sign-in is **Google OAuth only** (`src/app/sign-in/google-button.tsx`);
  there is no email/password and no magic link.
- **Viewer:** `lib/auth/viewer.ts` — `getViewer()` already carries `email`.
  `requireViewer()` gates on approval + setup via `lib/auth/gate.ts`.
- **The seven server read paths that implement "everyone":**
  `scoreboard`, `friendActivity`, `friendMocks` (`lib/tracker/me.ts`),
  `friendSummaryData` (`lib/coach/tools-data.ts:229`),
  `problemDetail` (`lib/library/queries.ts:106`),
  `notifyFriends` (`lib/push.ts:65`).
  **These are what actually enforce visibility** — Drizzle runs on a connection
  that bypasses RLS. Changing policies alone changes nothing.
- **The seven RLS select policies** reading `using (public.is_approved())`:
  `profiles_read` (access), `checkins_read_approved` (`…0004_checkin_notes.sql:36`),
  `campaigns_read_approved`, `days_read_approved`, `readiness_read_approved`
  (`…0006_tracker.sql:111-113`), `mocks_read_approved` (`…0010_coach.sql:136`).
- **Admin:** `src/app/admin/users/` — `page.tsx` joins `auth.users` for emails,
  `actions.ts` has `decide`.
- **No mail dependency and no central env module.** Each lib reads
  `process.env` with its own guard (see `searchKnowledge` in
  `lib/coach/tools-data.ts`). `lib/site-url.ts` is the equivalent of Curfew's
  `dashboardUrl()` — use it.
- **Gates you must keep green:** `check:rls` asserts the current
  everyone-sees-everyone behaviour in ~8 places (grep `friend` in
  `web/scripts/check-rls.ts` — lines 117-121, 166-169, 230-233, 275-276). Those
  assertions must be **rewritten**, not deleted: a friend reads, a non-friend
  does not.

## Build

### 1. Migration `supabase/migrations/20260929000018_friends.sql`

Two tables. Curfew's group invite shape, retargeted from a group to a pair.

```sql
create extension if not exists citext;

-- A pending request. The row IS the request: it is what the recipient's
-- dashboard lists, whether or not they ever open the email.
create table public.friend_invites (
    id           uuid primary key default gen_random_uuid(),
    email        citext not null,
    invited_by   uuid not null references auth.users (id) on delete cascade,
    status       text not null default 'pending'
                   check (status in ('pending', 'accepted', 'revoked')),
    created_at   timestamptz not null default now(),
    responded_at timestamptz,
    -- Dismissed means the recipient hid it. Still pending; the sender sees no
    -- change and a link in hand still works. It just stops being listed.
    dismissed_at timestamptz,
    check ((status = 'pending') = (responded_at is null))
);
-- One live invite per sender per address. This index is what makes a repeat
-- invite a silent no-op via `on conflict do nothing`.
create unique index friend_invites_pending_idx
    on public.friend_invites (invited_by, email) where status = 'pending';
create index friend_invites_email_idx on public.friend_invites (email) where status = 'pending';

-- One row per pair, ordered, so asymmetric visibility cannot drift into being.
create table public.friendships (
    user_a     uuid not null references auth.users (id) on delete cascade,
    user_b     uuid not null references auth.users (id) on delete cascade,
    created_at timestamptz not null default now(),
    from_invite uuid references public.friend_invites (id) on delete set null,
    primary key (user_a, user_b),
    check (user_a < user_b)
);
```

`check (user_a < user_b)` is the point. Do not model this as two directed rows —
one row per pair means "A sees B but B does not see A" is unrepresentable.

Then the helper every policy uses, `security definer` for the same reason
`is_approved()` is:

```sql
create function public.is_friend(other uuid) returns boolean
language sql stable security definer set search_path = ''
as $$
  select other = auth.uid() or exists (
    select 1 from public.friendships
    where (user_a = least(auth.uid(), other) and user_b = greatest(auth.uid(), other))
  );
$$;
```

It returns true for yourself, so every policy below reads the same way and no
caller needs an `or user_id = auth.uid()` clause.

**Rewrite the six cross-user select policies** to
`using (public.is_approved() and public.is_friend(user_id))`. Keep
`is_approved()` in the conjunction — a pending or rejected account must still
see nothing even if a friendship row somehow exists.

- `checkins_read_approved`, `campaigns_read_approved`, `days_read_approved`,
  `readiness_read_approved`, `mocks_read_approved`.
- `profiles_read` is different: it becomes
  `using (user_id = auth.uid() or public.is_friend(user_id))`, **and** the
  over-exposure in it gets fixed. A friend must not read
  `leetcode_username`, `notifications`, `campaign_days`, `role` or `language`.
  Column privileges are the tool: `revoke select on public.profiles from authenticated;`
  then `grant select (user_id, name, avatar_url) on public.profiles to authenticated;`
  and grant the full column list back for the owner's own row via a view or by
  keeping the server connection (which bypasses RLS) as the only reader of the
  private columns. **Pick one, and write the reasoning in the migration.** If
  column grants fight Drizzle's `select *` anywhere, the fallback is a
  `public.profiles_public` view (`user_id, name, avatar_url`) with
  `security_invoker = true` and pointing the friend-facing queries at it.

Policies for the new tables:

```sql
alter table public.friend_invites enable row level security;
alter table public.friendships enable row level security;

-- You see invites you sent and invites addressed to your own email.
create policy friend_invites_read on public.friend_invites for select to authenticated
  using (invited_by = auth.uid()
         or email = (select email from auth.users where id = auth.uid()));
create policy friend_invites_send on public.friend_invites for insert to authenticated
  with check (invited_by = auth.uid() and public.is_approved());
create policy friend_invites_respond on public.friend_invites for update to authenticated
  using (email = (select email from auth.users where id = auth.uid()) or invited_by = auth.uid());

-- You see your own friendships and nobody else's.
create policy friendships_read on public.friendships for select to authenticated
  using (user_a = auth.uid() or user_b = auth.uid());
```

**No backfill.** The owner chose to start empty: nobody is anyone's friend on
day one and scoreboards go blank until people invite each other. Say so in a
migration comment so nobody "fixes" it later.

### 2. `web/src/lib/email.ts` and `web/src/lib/email/templates.ts`

Add `resend` to `web/package.json` (Curfew is on `^6.25.0`). Two env vars,
`RESEND_API_KEY` and `EMAIL_FROM`, read with the same guard style as
`searchKnowledge`; add both to `.env.example` and to the Vercel project.

`lib/email.ts` — Curfew's, near-verbatim:

```ts
import { Resend } from "resend";

export type EmailInput = { to: string; subject: string; html: string; text: string };

export async function sendEmail(input: EmailInput): Promise<string | null> {
  const key = process.env.RESEND_API_KEY;
  const from = process.env.EMAIL_FROM;
  if (!key || !from) throw new Error("RESEND_API_KEY / EMAIL_FROM are not set");
  const { data, error } = await new Resend(key).emails.send({ from, ...input });
  if (error) throw new Error(error.message);
  return data?.id ?? null;
}
```

Plus `sendEmailBestEffort` exactly as quoted above.

**Templates.** Curfew's are table-based with inline styles, no web fonts, no
`<style>` block, because mail clients strip all three. Do the same in 90x's
house style, not Curfew's: dark `#0a0c10` background, surface `#0f1218`, text
`#e6e9ef`, mute `#7d8594`, accent `#67e8f9`, Sora/Manrope named with a system
sans fallback. The mark is drawn from table cells rather than an image — Curfew
builds its logo from 9px `<td>`s so it survives image blocking. Do the
equivalent for the 90x mark, or use the committed PNG at
`web/public/icons/icon-192.png` behind an absolute URL and accept it may be
blocked. **Escape every interpolated value** (`escapeHtml`) — an inviter's
display name comes from Google and is attacker-controlled.

Three templates, each returning `EmailInput`, each with a real `text` part:

- `friendInviteEmail(to, inviterName)` — *"{inviter} invited you to 90x."* →
  button to `siteUrl()` → *"Sign in with Google. Once your account is approved,
  accept the request from your dashboard."* Footer: *"90x is invite-only. You
  received this because someone entered your address."*
- `approvalEmail(to, approved)` — the approve path is the one that unblocks a
  pending invite, so it matters. Approved: *"Your 90x account has been
  approved."* → button. Not approved: one line, no button.
- Skip an `accountDisabledEmail` until there is a disable flow.

### 3. `web/src/lib/friends/service.ts`

Curfew's `inviteToGroup` logic, retargeted. Keep the two nonsense guards and the
`onConflictDoNothing` early return:

```ts
export async function invite(inviterId: string, rawEmail: string, q: Db = db): Promise<void> {
  const email = rawEmail.trim().toLowerCase();
  if (!email) throw new Error("Enter an email.");
  if (!EMAIL_RE.test(email)) throw new Error("That does not look like an email.");

  // If the address already has an account, guard the two nonsense cases.
  const [existing] = await q.execute(sql`select id from auth.users where lower(email) = ${email}`);
  if (existing) {
    if (existing.id === inviterId) throw new Error("You cannot invite yourself.");
    if (await areFriends(inviterId, existing.id, q)) throw new Error("You are already friends.");
  }

  const [row] = await q.insert(friendInvites)
    .values({ email, invitedBy: inviterId })
    .onConflictDoNothing()
    .returning({ id: friendInvites.id });
  if (!row) return;                       // already invited: silent no-op

  const [me] = await q.select({ name: profiles.name }).from(profiles).where(eq(profiles.userId, inviterId));
  await sendEmailBestEffort({ actorId: inviterId, kind: "invite",
    email: friendInviteEmail(email, me?.name ?? "Someone"), payload: { invite_id: row.id } });
}
```

Then, mirroring Curfew one-for-one:

- `pendingFor(email)` — `status = 'pending' and dismissed_at is null`, joined to
  the inviter's name. This is what the dashboard lists.
- `sentBy(inviterId)` — so the sender sees "invited a@b.com, not accepted yet"
  and can revoke.
- `accept(inviteId, userId, userEmail)` — re-check the email match, then in **one
  transaction** set `status = 'accepted'`, `responded_at = now()`, and insert the
  `friendships` row with `least`/`greatest` for the column order and
  `on conflict do nothing`.
- `refuse(inviteId, userEmail)` → `status = 'revoked'`, `responded_at = now()`.
- `dismiss(inviteId, userEmail)` → `dismissed_at = now()`, status untouched.
- `friendIds(viewerId, q)` → `string[]`, **including the viewer**, so callers
  can swap `innerJoin(userApprovals…)` for `inArray(x.userId, ids)` with no
  other change.
- `unfriend(viewerId, otherId)` — delete the pair row. The owner did not ask for
  it; add it anyway, because a friend graph with no exit is a trap.

**Add a cap.** Curfew has none, but 90x spends money per user on AI. Refuse past
20 pending invites per sender with a clear message, and put the number in one
named constant.

### 4. Replace the seven server read paths

All six of these keep their signatures; only the join changes.

- `lib/tracker/me.ts` — `scoreboard`, `friendActivity`, `friendMocks`: drop
  `innerJoin(userApprovals, …status = 'approved')` and use
  `inArray(profiles.userId, await friendIds(viewerId, q))`. Keep the
  `status = 'approved'` condition as well — an unapproved friend shows nothing.
  **Also fix the full-name leak:** `friendActivity` and `friendMocks` must
  return the first name only, the way `scoreboard` already does
  (`p.name.split(" ")[0]`). Do it in the query's select or in one shared helper;
  a component must not be the thing that decides.
- `lib/coach/tools-data.ts:229` `friendSummaryData` — already builds on
  `scoreboard`, so it follows for free. Confirm with a `check:coach-tools` case,
  don't assume.
- `lib/library/queries.ts:106` `problemDetail` — the `friends` list must be
  friends, first-name only.
- `lib/push.ts:65` `notifyFriends` — the broadcast. Restrict to
  `inArray(profiles.userId, friendIds)`; keep the 3-hour per-pair Redis cooldown
  as it is.

### 5. Screens

- **Invite form.** Curfew puts a confirm step in front of sending, because
  sending a real email that names you is not undoable:
  *"An email invite will be sent to {email}. It names you ({yourName}) as the
  inviter."* → Cancel / Send invite. Copy that. Live-validate with
  `/^[^@\s]+@[^@\s]+\.[^@\s]+$/` and disable Send until it passes. Put it on
  `/me` beside the scoreboard, with the sent-invite list under it.
- **Requests on the dashboard.** On `/today` (the owner said "dashboard" and
  `/today` is the landing screen) and on `/me`: one card per pending invite —
  *"{inviter} wants to compare progress"* — with **Accept**, **Refuse**,
  **Dismiss**. Refuse and Dismiss need the different-outcomes copy spelled out
  in a `title`/hint so the choice is legible.
- **Empty states.** `scoreboard.tsx:163` already has one for no activity. Add
  one for no friends at all that points at the invite form, and make the
  readiness dial and trend still render — those are the viewer's own data and
  must not disappear because they have no friends.
- Follow `.planning/SPEC.md` §7.4 and the existing components; do not restyle
  the scoreboard.

### 6. Admin

`src/app/admin/users/actions.ts` `decide`: on approve or reject, send
`approvalEmail` through `sendEmailBestEffort`. Approval currently tells the user
nothing, and it is now what stands between an invite and its acceptance.

## Verification

- **Rewrite `web/scripts/check-rls.ts`.** Its ~8 `friend` assertions currently
  prove the opposite of the new rule (grep `friend`; lines 117-121, 166-169,
  230-233, 275-276). For each of `checkins`, `days`, `campaigns`,
  `readiness_snapshots`, `mocks`, `profiles`: a **friend** reads, a **non-friend
  approved user reads zero rows**. Add: a non-friend cannot read
  `leetcode_username` or `notifications`; a pending user reads nothing even with
  a friendship row; `friend_invites` addressed to someone else is invisible; the
  `user_a < user_b` check rejects a reversed insert.
- **New `web/scripts/check-friends.ts`**, in the style of `check-feed.ts` (a
  `memoryStore`-shaped seam, no real Redis): invite → pending appears for that
  email only → accept creates exactly one `friendships` row → accepting twice is
  a no-op → refuse leaves no friendship → dismiss keeps it pending but unlisted
  → an invite for a different email throws → a repeat invite inserts nothing and
  sends no second email → the cap refuses at the limit. Wire it into
  `package.json` and the CI web job next to `check:feed`.
- `check:coach-tools` — `get_friend_summary` returns nothing for a user with no
  friends, and only the friend for a user with one.
- Unit tests for `friendIds` ordering and the `least`/`greatest` pair key.
- The full local gate set must pass: `typecheck lint test format:check
  check:tokens check:dead check:dupes check:cycles check:coverage`, `build` then
  `check:bundle`, plus `check:rls check:tracker check:feed check:friends
  check:coach-tools`, and the e2e suite including the axe scan. `resend` is
  server-only — if it lands in a client bundle, `check:bundle` will say so.
- **Playwright:** two signed-in users (`/api/test/sign-in` exists), each blind to
  the other, then invite → accept → each appears on the other's scoreboard.
- Update `.planning/SPEC.md` §3 Privacy: "Friends see…" now needs "a friend is
  someone you invited and who accepted, or who invited you".

## Do not

- Do not auto-approve invitees. The owner chose admin approval, and Curfew's
  email copy assumes it.
- Do not make the invite link a bearer token. See the top of this brief.
- Do not delete the `check:rls` friend assertions. Rewrite them.
- Do not leave `is_approved()` out of the conjunction on the six policies.
- Do not use Supabase's `inviteUserByEmail`. It creates an `auth.users` row with
  no identity, collides with Google-only sign-in, and its built-in SMTP is
  throttled to a few messages an hour.
