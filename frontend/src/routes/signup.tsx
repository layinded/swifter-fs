import {
    Button,
    Container,
    Divider,
    Flex,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Image,
    Input,
    Link,
    Text,
} from "@chakra-ui/react";
import {Link as RouterLink, createFileRoute, redirect} from "@tanstack/react-router";
import {type SubmitHandler, useForm} from "react-hook-form";

import Logo from "/assets/images/fastapi-logo.svg";
import type {UserRegister} from "../client";
import useAuth, {isLoggedIn} from "../hooks/useAuth";
import {emailPattern, passwordRules} from "../utils";
import SocialLoginButtons from "../components/Common/SocialLoginButtons";
import {useTranslationHelper} from "../utils/translationHelper";

export const Route = createFileRoute("/signup")({
    component: SignUp,
    beforeLoad: async () => {
        if (isLoggedIn()) {
            throw redirect({to: "/"});
        }
    },
});

interface UserRegisterForm extends UserRegister {
    confirm_password: string;
}

function SignUp() {
    const {signUpMutation, oauthUrls} = useAuth();
    const {
        register,
        handleSubmit,
        getValues,
        formState: {errors, isSubmitting},
    } = useForm<UserRegisterForm>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            email: "",
            full_name: "",
            password: "",
            confirm_password: "",
        },
    });

    const onSubmit: SubmitHandler<UserRegisterForm> = async (data) => {
        const {confirm_password, ...userData} = data;
        try {
            await signUpMutation.mutateAsync({requestBody: userData});
        } catch (error) {
            console.error("Signup failed", error);
        }
    };

    // Use the centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    return (
        <Flex flexDir={{base: "column", md: "row"}} justify="center" h="100vh">
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
                    alt={getTranslation("logo_alt")}
                    height="auto"
                    maxW="2xs"
                    alignSelf="center"
                    mb={4}
                />

                <FormControl id="full_name" isInvalid={!!errors.full_name}>
                    <FormLabel htmlFor="full_name">{getTranslation("form_label_full_name")}</FormLabel>
                    <Input
                        id="full_name"
                        minLength={3}
                        {...register("full_name", {required: getTranslation("form_validation_full_name_required")})}
                        placeholder={getTranslation("form_placeholder_full_name")}
                        type="text"
                        required
                    />
                    {errors.full_name && (
                        <FormErrorMessage>{errors.full_name.message}</FormErrorMessage>
                    )}
                </FormControl>

                <FormControl id="email" isInvalid={!!errors.email}>
                    <FormLabel htmlFor="email">{getTranslation("form_label_email")}</FormLabel>
                    <Input
                        id="email"
                        {...register("email", {
                            required: getTranslation("form_validation_email_required"),
                            pattern: emailPattern,
                        })}
                        placeholder={getTranslation("form_placeholder_email")}
                        type="email"
                        required
                    />
                    {errors.email && (
                        <FormErrorMessage>{errors.email.message}</FormErrorMessage>
                    )}
                </FormControl>

                <FormControl id="password" isInvalid={!!errors.password}>
                    <FormLabel htmlFor="password">{getTranslation("form_label_set_password")}</FormLabel>
                    <Input
                        id="password"
                        {...register("password", passwordRules())}
                        placeholder={getTranslation("form_placeholder_password")}
                        type="password"
                        required
                    />
                    {errors.password && (
                        <FormErrorMessage>{errors.password.message}</FormErrorMessage>
                    )}
                </FormControl>

                <FormControl id="confirm_password" isInvalid={!!errors.confirm_password}>
                    <FormLabel htmlFor="confirm_password">{getTranslation("form_label_confirm_password")}</FormLabel>
                    <Input
                        id="confirm_password"
                        {...register("confirm_password", {
                            required: getTranslation("form_validation_confirm_password_required"),
                            validate: (value) =>
                                value === getValues().password ||
                                getTranslation("form_validation_passwords_do_not_match"),
                        })}
                        placeholder={getTranslation("form_placeholder_confirm_password")}
                        type="password"
                        required
                    />
                    {errors.confirm_password && (
                        <FormErrorMessage>{errors.confirm_password.message}</FormErrorMessage>
                    )}
                </FormControl>

                <Button variant="primary" type="submit" isLoading={isSubmitting} isDisabled={isSubmitting}>
                    {getTranslation("button_save")}
                </Button>

                <Divider my={4}/>

                {/* Render shared SocialLoginButtons with customized button text */}
                <SocialLoginButtons oauthUrls={oauthUrls}/>

                <Text>
                    {getTranslation("login_already_have_account")}{" "}
                    <Link as={RouterLink} to="/login" color="blue.500">
                        {getTranslation("login_signin")}
                    </Link>
                </Text>
            </Container>
        </Flex>
    );
}

export default SignUp;
