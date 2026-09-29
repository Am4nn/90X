// The admin surface, listed here rather than discovered, ON PURPOSE.
//
// The admin actions themselves are session-based server actions (they derive
// the user from the cookie via requireViewer), so they cannot be called
// directly with a foreign id. What a stranger *can* touch is the routes, so the
// HTTP sweep (http.ts) probes each of these signed-out and asserts it never
// renders. A second list has to be updated by hand, and the completeness check
// in http.ts fails loudly when it has not been.
export const ADMIN_ROUTES: string[] = [
  "/admin",
  "/admin/users",
  "/admin/cards",
  "/admin/cards/flagged",
  "/admin/mail",
];

// One route with a path parameter each, so the sweep asks for a concrete row too.
export const ADMIN_PARAM_ROUTES: string[] = [
  "/admin/cards/00000000-0000-4000-8000-000000000000",
  "/admin/mail/00000000-0000-4000-8000-000000000000",
];
