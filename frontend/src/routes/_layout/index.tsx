import { Box, Container, Text } from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";

import useAuth from "../../hooks/useAuth";

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
});

function Dashboard() {
  const { user: currentUser } = useAuth();
  const displayName = currentUser?.full_name?.trim() || currentUser?.email || "Guest";

  return (
    <Container maxW="full">
      <Box pt={12} m={4}>
        <Text fontSize={{ base: "xl", md: "2xl" }} fontWeight="bold">
          Hi, {displayName} 👋🏼
        </Text>
        <Text color="gray.600" fontSize={{ base: "sm", md: "md" }}>
          Welcome back, nice to see you again!
        </Text>
      </Box>
    </Container>
  );
}

export default Dashboard;
