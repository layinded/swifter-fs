import { type Page, expect } from "@playwright/test";

export async function signUpNewUser(
  page: Page,
  name: string,
  email: string,
  password: string,
) {
  // Navigate to the signup page and wait for the DOM to be loaded
  await page.goto("/signup");
  await page.waitForLoadState("domcontentloaded");

  await page.getByPlaceholder("Full Name").fill(name);
  await page.getByPlaceholder("Email").fill(email);
  await page.getByPlaceholder("Password", { exact: true }).fill(password);
  await page.getByPlaceholder("Repeat Password").fill(password);

  await page.getByRole("button", { name: "Sign Up" }).click();

  // Assert that the success message is visible
  await expect(
    page.getByText("Your account has been created successfully"),
  ).toBeVisible();

  // Navigate to login page
  await page.goto("/login");
}

export async function logInUser(page: Page, email: string, password: string) {
  await page.goto("/login");
  await page.waitForLoadState("domcontentloaded");

  await page.getByPlaceholder("Email").fill(email);
  await page.getByPlaceholder("Password", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Log In" }).click();

  // Wait for navigation to the home page ("/")
  await page.waitForURL("/");
  await expect(
    page.getByText("Welcome back, nice to see you again!"),
  ).toBeVisible();
}

export async function logOutUser(page: Page) {
  // Click on the user menu and select "Log out"
  await page.getByTestId("user-menu").click();
  await page.getByRole("menuitem", { name: "Log out" }).click();

  // Wait for navigation to the login page and assert it
  await page.waitForURL("/login");
  await expect(page).toHaveURL("/login");
}
