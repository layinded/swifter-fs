import {ViewIcon, ViewOffIcon} from "@chakra-ui/icons";
import {
    Button,
    Container,
    Divider,
    FormControl,
    FormErrorMessage,
    Icon,
    Image,
    Input,
    InputGroup,
    InputRightElement,
    Link,
    Text,
    useBoolean,
} from "@chakra-ui/react";
import {Link as RouterLink, createFileRoute, redirect} from "@tanstack/react-router";
import {type SubmitHandler, useForm} from "react-hook-form";

import Logo from "/assets/images/fastapi-logo.svg";
import type {Body_Authentication_login_user as AccessToken} from "../client/types.gen";
import useAuth, {isLoggedIn} from "../hooks/useAuth";
import {emailPattern} from "../utils";
import SocialLoginButtons from "../components/Common/SocialLoginButtons";
import useCustomToast from "../hooks/useCustomToast";
import {useTranslationHelper} from "../utils/translationHelper";

export const Route = createFileRoute("/login")({
    component: Login,
    beforeLoad: async () => {
        if (isLoggedIn()) {
            throw redirect({to: "/"});
        }
    },
});

function Login() {
    const [show, setShow] = useBoolean();
    const {loginMutation, oauthUrls, error, resetError} = useAuth();
    const {
        register,
        handleSubmit,
        formState: {errors, isSubmitting},
    } = useForm<AccessToken>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            username: "",
            password: "",
        },
    });
    useCustomToast();
// Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    const onSubmit: SubmitHandler<AccessToken> = async (data) => {
        if (isSubmitting) return;
        resetError();
        try {
            await loginMutation.mutateAsync({formData: data});
        } catch {
            // Error is handled by the useAuth hook
        }
    };

    return (
        <Container
            as="form"
            onSubmit={handleSubmit(onSubmit)}
            h="100vh"
            maxW="sm"
            alignItems="stretch"
            justifyContent="center"
            gap={4}
            centerContent
        >
            <Image
                src={Logo}
                alt="FastAPI logo"
                height="auto"
                maxW="2xs"
                alignSelf="center"
                mb={4}
            />
            <FormControl id="username" isInvalid={!!errors.username || !!error}>
                <Input
                    id="username"
                    {...register("username", {
                        required: getTranslation("login_username_required"),
                        pattern: emailPattern,
                    })}
                    placeholder={getTranslation("login_email_or_username_placeholder")}
                    type="text"
                    aria-label={getTranslation("login_email_or_username_placeholder")}
                    required
                />
                {errors.username && (
                    <FormErrorMessage>{errors.username.message}</FormErrorMessage>
                )}
            </FormControl>
            <FormControl id="password" isInvalid={!!errors.password || !!error}>
                <InputGroup>
                    <Input
                        {...register("password", {
                            required: getTranslation("login_password_required"),
                        })}
                        type={show ? "text" : "password"}
                        placeholder={getTranslation("login_password_placeholder")}
                        required
                    />
                    <InputRightElement color="ui.dim" _hover={{cursor: "pointer"}}>
                        <Icon
                            as={show ? ViewOffIcon : ViewIcon}
                            onClick={setShow.toggle}
                            aria-label={show ? getTranslation("login_hide_password") : getTranslation("login_show_password")}
                        />
                    </InputRightElement>
                </InputGroup>
                {errors.password && (
                    <FormErrorMessage>{errors.password.message}</FormErrorMessage>
                )}
                {error && <FormErrorMessage>{error}</FormErrorMessage>}
            </FormControl>
            <Link as={RouterLink} to="/recover-password" color="blue.500">
                {getTranslation("login_forgot_password")}
            </Link>
            <Button
                variant="primary"
                type="submit"
                isLoading={isSubmitting}
                isDisabled={isSubmitting}
            >
                {getTranslation("login_button")}
            </Button>
            <Divider my={4}/>
            {/* SocialLoginButtons now renders the available providers based on oauthUrls */}
            <SocialLoginButtons oauthUrls={oauthUrls}/>
            <Text>
                {getTranslation("login_no_account")}{" "}
                <Link as={RouterLink} to="/signup" color="blue.500">
                    {getTranslation("login_signup")}
                </Link>
            </Text>
        </Container>
    );
}

export default Login;
