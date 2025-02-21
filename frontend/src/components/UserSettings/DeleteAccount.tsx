import {
    Button,
    Container,
    Heading,
    Text,
    useDisclosure,
} from "@chakra-ui/react";
import DeleteConfirmation from "./DeleteConfirmation";
import {useTranslationHelper} from "../../utils/translationHelper";

const DeleteAccount = () => {
    const confirmationModal = useDisclosure();

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) return <p>Loading translations...</p>;

    return (
        <Container maxW="full">
            <Heading size="sm" py={4}>
                {getTranslation("delete_account_heading")}
            </Heading>
            <Text>
                {getTranslation("delete_account_text")}
            </Text>
            <Button
                variant="solid"
                colorScheme="red"
                mt={4}
                onClick={confirmationModal.onOpen}
            >
                {getTranslation("delete_account_button")}
            </Button>
            <DeleteConfirmation
                isOpen={confirmationModal.isOpen}
                onClose={confirmationModal.onClose}
            />
        </Container>
    );
};

export default DeleteAccount;
