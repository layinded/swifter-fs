// src/components/UserSettings/DeleteAccount.tsx
import {
  Button,
  Container,
  Heading,
  Text,
  useDisclosure,
} from "@chakra-ui/react";

import DeleteConfirmation from "./DeleteConfirmation";

const DeleteAccount = () => {
  const confirmationModal = useDisclosure();

  return (
    <Container maxW="full">
      <Heading size="sm" py={4}>
        Delete Account
      </Heading>
      <Text>
        Permanently delete your data and everything associated with your
        account. This action cannot be undone.
      </Text>
      <Button
        variant="solid"
        colorScheme="red"
        mt={4}
        onClick={confirmationModal.onOpen}
      >
        Delete Account
      </Button>
      <DeleteConfirmation
        isOpen={confirmationModal.isOpen}
        onClose={confirmationModal.onClose}
      />
    </Container>
  );
};

export default DeleteAccount;
