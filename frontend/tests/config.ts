import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables from the .env file two levels up
dotenv.config({ path: path.join(__dirname, "../../.env") });

// Destructure required environment variables
const { FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD } = process.env;

// Validate that the required environment variables are defined
if (!FIRST_SUPERUSER) {
  throw new Error("Environment variable FIRST_SUPERUSER is undefined");
}

if (!FIRST_SUPERUSER_PASSWORD) {
  throw new Error("Environment variable FIRST_SUPERUSER_PASSWORD is undefined");
}

// Export the values for use in tests
export const firstSuperuser = FIRST_SUPERUSER;
export const firstSuperuserPassword = FIRST_SUPERUSER_PASSWORD;
