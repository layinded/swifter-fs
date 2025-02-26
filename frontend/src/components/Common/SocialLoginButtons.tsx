import {Button, Flex} from "@chakra-ui/react";
import {FaGoogle, FaFacebook} from "react-icons/fa";
import {useTranslationHelper} from "../../utils/translationHelper";

interface SocialLoginButtonsProps {
    oauthUrls: {
        google?: string | null;
        facebook?: string | null;
        github?: string | null;
    };
    buttonTextPrefix?: string;
}

const SocialLoginButtons = ({oauthUrls}: SocialLoginButtonsProps) => {
    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <Flex direction="column" gap={3}>Loading translations...</Flex>;
    }

    return (
        <Flex direction="column" gap={3}>
            {oauthUrls.google && (
                <Button
                    leftIcon={<FaGoogle/>}
                    variant="outline"
                    w="full"
                    as="a"
                    href={oauthUrls.google}
                >
                    {getTranslation("social_continue_with_google")}
                </Button>
            )}
            {oauthUrls.facebook && (
                <Button
                    leftIcon={<FaFacebook/>}
                    variant="outline"
                    w="full"
                    colorScheme="facebook"
                    as="a"
                    href={oauthUrls.facebook}
                >
                    {getTranslation("social_continue_with_facebook")}
                </Button>
            )}
        </Flex>
    );
};

export default SocialLoginButtons;
