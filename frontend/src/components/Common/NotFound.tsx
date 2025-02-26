import {Button, Container, Text} from "@chakra-ui/react";
import {Link} from "@tanstack/react-router";
import {useTranslationHelper} from "../../utils/translationHelper";

const NotFound = () => {
    // Use the centralized translation helper
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) return <p>Loading translations...</p>;

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
            <Text fontSize="md" mb={2}>
                {getTranslation("notfound_oops")}
            </Text>
            <Text fontSize="md" mb={4}>
                {getTranslation("notfound_page_not_found")}
            </Text>
            <Button as={Link} to="/" colorScheme="teal" variant="outline">
                {getTranslation("notfound_button_go_back")}
            </Button>
        </Container>
    );
};

export default NotFound;
