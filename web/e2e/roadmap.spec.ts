import { expect, test } from "@playwright/test";
import { signIn } from "./helpers";

const view = (page: import("@playwright/test").Page) => page.getByRole("navigation", { name: "View" });

test("a non-DSA area shows the toggle and opens on List", async ({ page }) => {
  await signIn(page, "roadmap", { next: "/library?area=system_design" });
  await expect(view(page)).toBeVisible();
  await expect(view(page).getByRole("link", { name: "List" })).toHaveAttribute("aria-current", "page");
  await expect(page.getByRole("heading", { name: "Roadmap", exact: true })).toBeVisible();
});

test("Roadmap renders the graph, keeps ?view=roadmap on reload, and links only real lessons", async ({ page }) => {
  await signIn(page, "roadmap", { next: "/library?area=system_design" });
  await view(page).getByRole("link", { name: "Roadmap" }).click();
  await expect(page).toHaveURL(/view=roadmap/);
  const graph = page.getByRole("region", { name: /roadmap$/ }).first();
  await expect(graph).toBeVisible();

  await page.reload();
  await expect(page).toHaveURL(/view=roadmap/);
  await expect(view(page).getByRole("link", { name: "Roadmap" })).toHaveAttribute("aria-current", "page");
  await expect(graph).toBeVisible();

  const lesson = graph.locator('a[href^="/library/topic/"]').first();
  await expect(lesson).toBeVisible();
  const href = await lesson.getAttribute("href");
  await lesson.click();
  await expect(page).toHaveURL(href ?? "");

  await page.goBack();
  const soon = page.getByText("soon", { exact: true }).first();
  if (await soon.count()) {
    const row = soon.locator("xpath=..");
    await expect(row.getByRole("link")).toHaveCount(0);
    await expect(row.getByRole("button")).toBeVisible();
  }
});

test("a tick made in the Roadmap view survives a reload", async ({ page }) => {
  await signIn(page, "roadmap", { next: "/library?area=system_design&view=roadmap" });
  const tick = page.getByRole("button", { name: /^Mark .* as covered$/ }).first();
  const name = (await tick.getAttribute("aria-label")) ?? "";
  // The tick is optimistic: the row flips before tickRoadmapNodeAction returns, and a
  // reload that beats the write aborts the action's own POST, so the tick is lost and
  // reloading again cannot bring it back. Waiting for that POST is the difference
  // between asserting the write happened and asserting the button changed colour.
  const written = page.waitForResponse((r) => r.request().method() === "POST" && r.ok());
  await tick.click();
  const ticked = page.getByRole("button", { name: name.replace("as covered", "as not covered") });
  await expect(ticked).toHaveAttribute("aria-pressed", "true");
  await written;
  await page.reload();
  await expect(ticked).toHaveAttribute("aria-pressed", "true");
});

test("DSA has no toggle and keeps its Pattern Map", async ({ page }) => {
  await signIn(page, "roadmap", { next: "/library?area=dsa" });
  await expect(view(page)).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Patterns" })).toBeVisible();
});
