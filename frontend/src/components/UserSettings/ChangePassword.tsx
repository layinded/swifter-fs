import {
    Button,
    Container,
    Heading,
    Box,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Text,
    useColorModeValue,
} from "@chakra-ui/react";
import {useMutation} from "@tanstack/react-query";
import {type SubmitHandler, useForm} from "react-hook-form";

import {type UpdatePassword} from "../../client";
import {AuthenticationService} from "../../client";
import type {ApiError} from "../../client";
import useCustomToast from "../../hooks/useCustomToast";
import useAuth from "../../hooks/useAuth";
import {handleError, passwordRules} from "../../utils";
import {useTranslationHelper} from "../../utils/translationHelper";

interface UpdatePasswordForm extends UpdatePassword {
    confirm_password: string;
}

const ChangePassword = () => {
    const {user} = useAuth();
    const color = useColorModeValue("inherit", "ui.light");
    const showToast = useCustomToast();

    // Use the centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    // If the user signed up via social login, disable password change.
    if (user && user.auth_provider && user.auth_provider !== "local") {
        return (
            <Container maxW="full" py={4}>
                <Heading size="sm" mb={4}>
                    {getTranslation("change_password_heading")}
                </Heading>
                <Text>{getTranslation("change_password_social_error")}</Text>
            </Container>
        );
    }

    const {
        register,
        handleSubmit,
        reset,
        getValues,
        formState: {errors, isSubmitting},
    } = useForm<UpdatePasswordForm>({
        mode: "onBlur",
        criteriaMode: "all",
    });

    const mutation = useMutation({
        mutationFn: (data: UpdatePassword) =>
            AuthenticationService.changePassword({requestBody: data}),
        onSuccess: () => {
            showToast(
                getTranslation("change_password_success_title"),
                getTranslation("change_password_success_message"),
                "success"
            );
            reset();
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
    });

    const onSubmit: SubmitHandler<UpdatePasswordForm> = async (data) => {
        mutation.mutate(data);
    };

    return (
        <Container maxW="full">
            <Heading size="sm" py={4}>
                {getTranslation("change_password_heading")}
            </Heading>
            <Box
                w={{sm: "full", md: "50%"}}
                as="form"
                onSubmit={handleSubmit(onSubmit)}
            >
                <FormControl isRequired isInvalid={!!errors.current_password}>
                    <FormLabel color={color} htmlFor="current_password">
                        {getTranslation("form_label_current_password")}
                    </FormLabel>
                    <Input
                        id="current_password"
                        {...register("current_password", {
                            required: getTranslation("form_validation_current_password_required"),
                        })}
                        placeholder={getTranslation("form_placeholder_current_password")}
                        type="password"
                        w="auto"
                    />
                    {errors.current_password && (
                        <FormErrorMessage>
                            {errors.current_password.message}
                        </FormErrorMessage>
                    )}
                </FormControl>
                <FormControl mt={4} isRequired isInvalid={!!errors.new_password}>
                    <FormLabel htmlFor="new_password">
                        {getTranslation("form_label_new_password")}
                    </FormLabel>
                    <Input
                        id="new_password"
                        {...register("new_password", passwordRules())}
                        placeholder={getTranslation("form_placeholder_new_password")}
                        type="password"
                        w="auto"
                    />
                    {errors.new_password && (
                        <FormErrorMessage>
                            {errors.new_password.message}
                        </FormErrorMessage>
                    )}
                </FormControl>
                <FormControl mt={4} isRequired isInvalid={!!errors.confirm_password}>
                    <FormLabel htmlFor="confirm_password">
                        {getTranslation("form_label_confirm_password")}
                    </FormLabel>
                    <Input
                        id="confirm_password"
                        {...register("confirm_password", {
                            validate: (value) =>
                                value === getValues().new_password ||
                                getTranslation("form_validation_passwords_do_not_match"),
                        })}
                        placeholder={getTranslation("form_placeholder_confirm_password")}
                        type="password"
                        w="auto"
                    />
                    {errors.confirm_password && (
                        <FormErrorMessage>
                            {errors.confirm_password.message}
                        </FormErrorMessage>
                    )}
                </FormControl>
                <Button variant="primary" mt={4} type="submit" isLoading={isSubmitting}>
                    {getTranslation("button_save")}
                </Button>
            </Box>
        </Container>
    );
};

export default ChangePassword;
