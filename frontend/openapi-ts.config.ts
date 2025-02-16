import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  client: "legacy/axios",
  input: "./openapi.json",
  output: "./src/client",
  exportSchemas: true,
  plugins: [
    "@hey-api/schemas",
    {
      name: "@hey-api/sdk",
      asClass: true,
      operationId: true,
      transformer: true,
      methodNameBuilder: (operation) => {
        const name = operation.name || operation.operationId || "unknownOperation";
        return `${name.charAt(0).toLowerCase()}${name.slice(1)}`;
      },
    },
  ],
});
