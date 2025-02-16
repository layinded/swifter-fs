// src/components/common/NotFound.tsx
import { Button, Container, Text } from "@chakra-ui/react";
import { Link } from "@tanstack/react-router";

const NotFound = () => {
  return (
    <Container
      h="100vh"
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      textAlign="center"
      maxW="sm"
    >
      <Text fontSize="8xl" color="ui.main" fontWeight="bold" lineHeight="1" mb={4}>
        404
      </Text>
      <Text fontSize="md" mb={2}>Oops!</Text>
      <Text fontSize="md" mb={4}>Page not found.</Text>
      <Button as={Link} to="/" colorScheme="teal" variant="outline">
        Go back
      </Button>
    </Container>
  );
};

export default NotFound;
