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
import {
    Link as RouterLink,
    createFileRoute,
    redirect,
} from "@tanstack/react-router";
import {type SubmitHandler, useForm} from "react-hook-form";

import Logo from "/assets/images/fastapi-logo.svg";
import type {Body_Authentication_login_user as AccessToken} from "../client/types.gen";
import useAuth, {isLoggedIn} from "../hooks/useAuth";
import {emailPattern} from "../utils";
import SocialLoginButtons from "../components/Common/SocialLoginButtons";

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
                        required: "Username or Email is required",
                        pattern: emailPattern,
                    })}
                    placeholder="Email or Username"
                    type="text"
                    aria-label="Enter your username or email"
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
                            required: "Password is required",
                        })}
                        type={show ? "text" : "password"}
                        placeholder="Password"
                        required
                    />
                    <InputRightElement color="ui.dim" _hover={{cursor: "pointer"}}>
                        <Icon
                            as={show ? ViewOffIcon : ViewIcon}
                            onClick={setShow.toggle}
                            aria-label={show ? "Hide password" : "Show password"}
                        />
                    </InputRightElement>
                </InputGroup>
                {errors.password && (
                    <FormErrorMessage>{errors.password.message}</FormErrorMessage>
                )}
                {error && <FormErrorMessage>{error}</FormErrorMessage>}
            </FormControl>
            <Link as={RouterLink} to="/recover-password" color="blue.500">
                Forgot password?
            </Link>
            <Button
                variant="primary"
                type="submit"
                isLoading={isSubmitting}
                isDisabled={isSubmitting}
            >
                Log In
            </Button>
            <Divider my={4}/>
            {/* SocialLoginButtons now renders the available providers based on oauthUrls */}
           <SocialLoginButtons oauthUrls={oauthUrls} />
            <Text>
                Don't have an account?{" "}
                <Link as={RouterLink} to="/signup" color="blue.500">
                    Sign up
                </Link>
            </Text>
        </Container>
    );
}

export default Login;
