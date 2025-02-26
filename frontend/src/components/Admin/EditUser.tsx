import {
    Button,
    Checkbox,
    Flex,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,

} from "@chakra-ui/react";
import {useMutation, useQueryClient} from "@tanstack/react-query";
import {type SubmitHandler, useForm} from "react-hook-form";

import {type UserUpdate, type UserPublic} from "../../client";
import {AdminService} from "../../client";
import type {ApiError} from "../../client";
import useCustomToast from "../../hooks/useCustomToast";
import {emailPattern, handleError} from "../../utils";
import {useTranslationHelper} from "../../utils/translationHelper";

interface EditUserProps {
    user: UserPublic;
    isOpen: boolean;
    onClose: () => void;
}

interface UserUpdateForm extends Omit<UserUpdate, "is_superuser" | "is_active"> {
    confirm_password: string;
    is_superuser: boolean;
    is_active: boolean;
}

const EditUser = ({user, isOpen, onClose}: EditUserProps) => {
    const queryClient = useQueryClient();
    const showToast = useCustomToast();

    const {
        register,
        handleSubmit,
        reset,
        getValues,
        formState: {errors, isSubmitting, isDirty},
    } = useForm<UserUpdateForm>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            email: user.email,
            full_name: user.full_name || "",
            password: "",
            confirm_password: "",
            is_superuser: user.is_superuser,
            is_active: user.is_active,
        },
    });

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    const mutation = useMutation({
        mutationFn: (data: UserUpdateForm) =>
            AdminService.updateUser({
                userId: user.id,
                requestBody: {
                    email: data.email,
                    full_name: data.full_name,
                    password: data.password || undefined, // Prevent sending an empty password
                    is_superuser: data.is_superuser,
                    is_active: data.is_active,
                },
            }),
        onSuccess: () => {
            showToast(
                getTranslation("success"),
                getTranslation("user_updated_successfully"),
                "success"
            );
            onClose();
            queryClient.invalidateQueries({queryKey: ["users"]});
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
    });

    const onSubmit: SubmitHandler<UserUpdateForm> = async (data) => {
        mutation.mutate(data);
    };

    const onCancel = () => {
        reset();
        onClose();
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} size={{base: "sm", md: "md"}} isCentered>
            <ModalOverlay/>
            <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
                <ModalHeader>{getTranslation("edit_user_modal_header")}</ModalHeader>
                <ModalCloseButton/>
                <ModalBody pb={6}>
                    <FormControl isInvalid={!!errors.email}>
                        <FormLabel htmlFor="email">{getTranslation("form_label_email")}</FormLabel>
                        <Input
                            id="email"
                            {...register("email", {
                                required: getTranslation("form_validation_email_required"),
                                pattern: emailPattern,
                            })}
                            placeholder={getTranslation("form_placeholder_email")}
                            type="email"
                        />
                        {errors.email && <FormErrorMessage>{errors.email.message}</FormErrorMessage>}
                    </FormControl>
                    <FormControl mt={4}>
                        <FormLabel htmlFor="full_name">{getTranslation("form_label_full_name")}</FormLabel>
                        <Input
                            id="full_name"
                            {...register("full_name")}
                            placeholder={getTranslation("form_placeholder_full_name")}
                            type="text"
                        />
                    </FormControl>
                    <FormControl mt={4} isInvalid={!!errors.password}>
                        <FormLabel htmlFor="password">{getTranslation("form_label_set_new_password")}</FormLabel>
                        <Input
                            id="password"
                            {...register("password", {
                                minLength: {
                                    value: 8,
                                    message: getTranslation("form_validation_password_min_length"),
                                },
                            })}
                            placeholder={getTranslation("form_placeholder_new_password")}
                            type="password"
                        />
                        {errors.password && <FormErrorMessage>{errors.password.message}</FormErrorMessage>}
                    </FormControl>
                    <FormControl mt={4} isInvalid={!!errors.confirm_password}>
                        <FormLabel htmlFor="confirm_password">
                            {getTranslation("form_label_confirm_password")}
                        </FormLabel>
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
                        />
                        {errors.confirm_password && (
                            <FormErrorMessage>{errors.confirm_password.message}</FormErrorMessage>
                        )}
                    </FormControl>
                    <Flex mt={4}>
                        <FormControl mt={4}>
                            <Checkbox {...register("is_superuser")} colorScheme="teal">
                                {getTranslation("checkbox_is_admin")}
                            </Checkbox>
                        </FormControl>
                        <FormControl mt={4}>
                            <Checkbox {...register("is_active")} colorScheme="teal">
                                {getTranslation("checkbox_is_active")}
                            </Checkbox>
                        </FormControl>
                    </Flex>
                </ModalBody>

                <ModalFooter gap={3}>
                    <Button variant="primary" type="submit" isLoading={isSubmitting} isDisabled={!isDirty}>
                        {getTranslation("button_save")}
                    </Button>
                    <Button onClick={onCancel}>{getTranslation("button_cancel")}</Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
};

export default EditUser;
