import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  client: "legacy/axios", // ✅ Use this for Axios instead of @hey-api/client-axios
  input: "./openapi.json",
  output: "./src/client",
  exportSchemas: true,
  plugins: [
    "@hey-api/schemas", // ✅ Ensures schemas.gen.ts is generated
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
