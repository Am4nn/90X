import { expect, type Page, test } from "@playwright/test";
import { gotoToday, missions, signIn } from "./helpers";

// Spec §3: Today is readable offline. The Feed's offline cards need Redis,
// which this job doesn't run yet, so they aren't covered here.

const offlineBanner = (page: Page) => page.getByText(/^You're offline\. Showing today as of \d{2}:\d{2}\.$/);

test("Today stays readable offline, with mission actions locked", { tag: "@mobile" }, async ({ page, context }) => {
  await signIn(page, "offline");
  await expect(missions(page)).toBeVisible();

  // The open page loses its connection.
  await context.setOffline(true);
  await expect(offlineBanner(page)).toBeVisible();
  for (const action of await missions(page).getByRole("button").all()) await expect(action).toBeDisabled();
  await context.setOffline(false);
  await expect(offlineBanner(page)).toBeHidden();

  // With the service worker in control, an online visit keeps a copy of the page...
  await page.evaluate(async () => {
    await navigator.serviceWorker.ready;
  });
  await gotoToday(page);
  await expect
    .poll(() => page.evaluate(async () => Boolean(await caches.match("/today", { ignoreVary: true }))), { timeout: 10_000 })
    .toBe(true);

  // ...which is what a reload shows offline.
  await context.setOffline(true);
  await page.reload();
  await expect(offlineBanner(page)).toBeVisible();
  await expect(missions(page).getByRole("listitem").first()).toBeVisible();
  await context.setOffline(false);
});
