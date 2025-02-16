import {Button, Flex} from "@chakra-ui/react";
import {FaGoogle, FaFacebook} from "react-icons/fa";

interface SocialLoginButtonsProps {
    oauthUrls: {
        google?: string | null;
        facebook?: string | null;
        github?: string | null;
    };
    buttonTextPrefix?: string;
}


const SocialLoginButtons = ({oauthUrls}: SocialLoginButtonsProps) => {
    // If the backend disables social logins, the endpoint should return null/empty values.
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
                    Continue with Google
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
                    Continue with Facebook
                </Button>
            )}
        </Flex>
    );
};

export default SocialLoginButtons;
