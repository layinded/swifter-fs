import { createFileRoute } from "@tanstack/react-router";
import OAuthSuccess from "../components/Common/OAuthSuccess"; // Create this component

export const Route = createFileRoute("/oauth-success")({
    component: OAuthSuccess,
});
