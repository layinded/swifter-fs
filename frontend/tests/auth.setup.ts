import { test as setup, expect } from "@playwright/test";
import { firstSuperuser, firstSuperuserPassword } from "./config.ts";

const authFile = "playwright/.auth/user.json";

setup("authenticate", async ({ page }) => {
  // Navigate to the login page and wait until the DOM is loaded.
  await page.goto("/login");
  await page.waitForLoadState("domcontentloaded");

  // Fill in the login form.
  await page.getByPlaceholder("Email").fill(firstSuperuser);
  await page.getByPlaceholder("Password").fill(firstSuperuserPassword);

  // Click the Log In button.
  await page.getByRole("button", { name: "Log In" }).click();

  // Wait for the URL to change to the home page.
  await page.waitForURL("/");

  // Optionally, assert that the login was successful.
  await expect(page).toHaveURL("/");

  // Save the storage state to reuse authenticated context in other tests.
  await page.context().storageState({ path: authFile });
});
