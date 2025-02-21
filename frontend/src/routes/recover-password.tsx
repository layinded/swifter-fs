import {
    Button,
    Container,
    FormControl,
    FormErrorMessage,
    Heading,
    Input,
    Text,
} from "@chakra-ui/react";
import {useMutation} from "@tanstack/react-query";
import {createFileRoute, redirect} from "@tanstack/react-router";
import {type SubmitHandler, useForm} from "react-hook-form";

import {type ApiError} from "../client/core/ApiError";
import {AuthenticationService} from "../client/sdk.gen";
import {isLoggedIn} from "../hooks/useAuth";
import useCustomToast from "../hooks/useCustomToast";
import {emailPattern, handleError} from "../utils";
import {useTranslationHelper} from "../utils/translationHelper";

export const Route = createFileRoute("/recover-password")({
    component: RecoverPassword,
    beforeLoad: async () => {
        if (isLoggedIn()) {
            throw redirect({to: "/"});
        }
    },
});

interface FormData {
    email: string;
}

function RecoverPassword() {
    const {
        register,
        handleSubmit,
        reset,
        formState: {errors, isSubmitting},
    } = useForm<FormData>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {email: ""},
    });

    const showToast = useCustomToast();

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    const mutation = useMutation({
        mutationFn: async (data: FormData) => {
            await AuthenticationService.authenticationRecoverPassword(data);
        },
        onSuccess: () => {
            showToast(
                getTranslation("recover_email_sent_title"),
                getTranslation("recover_email_sent_message"),
                "success"
            );
            reset();
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
    });

    const onSubmit: SubmitHandler<FormData> = async (data) => {
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
                {getTranslation("recover_password_heading")}
            </Heading>
            <Text align="center">
                {getTranslation("recover_password_text")}
            </Text>
            <FormControl isInvalid={!!errors.email}>
                <Input
                    id="email"
                    {...register("email", {
                        required: getTranslation("recover_email_required"),
                        pattern: emailPattern,
                    })}
                    placeholder={getTranslation("recover_email_placeholder")}
                    type="email"
                />
                {errors.email && (
                    <FormErrorMessage>{errors.email.message}</FormErrorMessage>
                )}
            </FormControl>
            <Button
                variant="primary"
                type="submit"
                isLoading={isSubmitting}
                isDisabled={isSubmitting}
            >
                {getTranslation("recover_reset_link_button")}
            </Button>
        </Container>
    );
}

export default RecoverPassword;
