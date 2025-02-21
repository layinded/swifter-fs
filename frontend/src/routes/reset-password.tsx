import {
    Button,
    Container,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Heading,
    Input,
    Text,
} from "@chakra-ui/react";
import {useMutation} from "@tanstack/react-query";
import {createFileRoute, redirect, useNavigate} from "@tanstack/react-router";
import {type SubmitHandler, useForm} from "react-hook-form";

import {type ApiError} from "../client/core/ApiError";
import {AuthenticationService} from "../client/sdk.gen";
import {isLoggedIn} from "../hooks/useAuth";
import useCustomToast from "../hooks/useCustomToast";
import {confirmPasswordRules, handleError, passwordRules} from "../utils";
import {useTranslationHelper} from "../utils/translationHelper";

export const Route = createFileRoute("/reset-password")({
    component: ResetPassword,
    beforeLoad: async () => {
        if (isLoggedIn()) {
            throw redirect({to: "/"});
        }
    },
});

interface NewPasswordForm {
    new_password: string;
    confirm_password: string;
}

function ResetPassword() {
    const {
        register,
        handleSubmit,
        getValues,
        reset,
        formState: {errors, isSubmitting},
    } = useForm<NewPasswordForm>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {new_password: ""},
    });

    const showToast = useCustomToast();
    const navigate = useNavigate();

    // Use the centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    // Move useMutation above the conditional return so it's always called.
    const mutation = useMutation({
        mutationFn: async (data: { new_password: string }) => {
            const token = new URLSearchParams(window.location.search).get("token");
            if (!token) {
                throw new Error("Invalid or missing token.");
            }
            await AuthenticationService.authenticationResetPassword({
                requestBody: {new_password: data.new_password, token},
            });
        },
        onSuccess: () => {
            showToast(
                getTranslation("reset_success_title"),
                getTranslation("reset_success_message"),
                "success"
            );
            reset();
            navigate({to: "/login"});
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
    });

    // Now, regardless of translations loading or not, all hooks have already been called.
    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    const onSubmit: SubmitHandler<NewPasswordForm> = async (data) => {
        mutation.mutate(data);
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
            <Heading size="xl" color="ui.main" textAlign="center" mb={2}>
                {getTranslation("reset_password_heading")}
            </Heading>
            <Text textAlign="center">{getTranslation("reset_password_text")}</Text>
            <FormControl mt={4} isInvalid={!!errors.new_password}>
                <FormLabel htmlFor="password">
                    {getTranslation("reset_new_password_label")}
                </FormLabel>
                <Input
                    id="password"
                    {...register("new_password", passwordRules())}
                    placeholder={getTranslation("reset_new_password_placeholder")}
                    type="password"
                />
                {errors.new_password && (
                    <FormErrorMessage>{errors.new_password.message}</FormErrorMessage>
                )}
            </FormControl>
            <FormControl mt={4} isInvalid={!!errors.confirm_password}>
                <FormLabel htmlFor="confirm_password">
                    {getTranslation("reset_confirm_password_label")}
                </FormLabel>
                <Input
                    id="confirm_password"
                    {...register("confirm_password", confirmPasswordRules(getValues))}
                    placeholder={getTranslation("reset_confirm_password_placeholder")}
                    type="password"
                />
                {errors.confirm_password && (
                    <FormErrorMessage>{errors.confirm_password.message}</FormErrorMessage>
                )}
            </FormControl>
            <Button
                variant="primary"
                type="submit"
                isLoading={isSubmitting}
                isDisabled={isSubmitting}
            >
                {getTranslation("reset_password_button")}
            </Button>
        </Container>
    );
}

export default ResetPassword;
