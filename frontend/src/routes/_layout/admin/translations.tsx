// src/routes/_layout/admin/translations.tsx
import {createFileRoute} from "@tanstack/react-router";
import AdminTranslations from "../../../components/Admin/AdminTranslations";

// Removed useAuth from here because hooks cannot be used in beforeLoad.
export const Route = createFileRoute("/_layout/admin/translations")({
    component: AdminTranslations,
    beforeLoad: async () => {
        // If you need an authentication check here, use a synchronous, non-hook method
        // (for example, reading from localStorage or a custom non-hook auth service)
        // Otherwise, rely on the check in AdminTranslations.
    },
});

export default AdminTranslations;
