import {Box, Container, Text} from "@chakra-ui/react";
import {createFileRoute} from "@tanstack/react-router";
import useAuth from "../../hooks/useAuth";
import {useTranslationHelper} from "../../utils/translationHelper";

export const Route = createFileRoute("/_layout/")({
    component: Dashboard,
});

function Dashboard() {
    const {user: currentUser} = useAuth();
    const displayName =
        currentUser?.full_name?.trim() || currentUser?.email || "Guest";

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    // Resolve translations using placeholders as needed.
    const greeting = getTranslation("dashboard_hi", {name: displayName});
    const welcomeMsg = getTranslation("dashboard_welcome_back");

    return (
        <Container maxW="full">
            <Box pt={12} m={4}>
                <Text fontSize={{base: "xl", md: "2xl"}} fontWeight="bold">
                    {greeting}
                </Text>
                <Text color="gray.600" fontSize={{base: "sm", md: "md"}}>
                    {welcomeMsg}
                </Text>
            </Box>
        </Container>
    );
}

export default Dashboard;
