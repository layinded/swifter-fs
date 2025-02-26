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

import {type UserCreate} from "../../client";
import {AdminService} from "../../client";
import type {ApiError} from "../../client";
import useCustomToast from "../../hooks/useCustomToast";
import {emailPattern, handleError} from "../../utils";
import {useTranslationHelper} from "../../utils/translationHelper";

interface AddUserProps {
    isOpen: boolean;
    onClose: () => void;
}

interface UserCreateForm extends Omit<UserCreate, "is_superuser" | "is_active"> {
    confirm_password: string;
    is_superuser: boolean;
    is_active: boolean;
}

const AddUser = ({isOpen, onClose}: AddUserProps) => {
    const queryClient = useQueryClient();
    const showToast = useCustomToast();
    const {
        register,
        handleSubmit,
        reset,
        getValues,
        formState: {errors, isSubmitting},
    } = useForm<UserCreateForm>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            email: "",
            full_name: "",
            password: "",
            confirm_password: "",
            is_superuser: false,
            is_active: true,
        },
    });

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    const mutation = useMutation({
        mutationFn: (data: UserCreateForm) =>
            AdminService.createUser({
                requestBody: {
                    email: data.email,
                    full_name: data.full_name,
                    password: data.password,
                    is_superuser: data.is_superuser,
                    is_active: data.is_active,
                },
            }),
        onSuccess: () => {
            showToast(
                getTranslation("success"),
                getTranslation("user_created_successfully"),
                "success"
            );
            reset();
            onClose();
            queryClient.invalidateQueries({queryKey: ["users"]});
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
    });

    const onSubmit: SubmitHandler<UserCreateForm> = (data) => {
        mutation.mutate(data);
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} size={{base: "sm", md: "md"}} isCentered>
            <ModalOverlay/>
            <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
                <ModalHeader>{getTranslation("add_user_modal_header")}</ModalHeader>
                <ModalCloseButton/>
                <ModalBody pb={6}>
                    <FormControl isRequired isInvalid={!!errors.email}>
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
                        {errors.email && (
                            <FormErrorMessage>{errors.email.message}</FormErrorMessage>
                        )}
                    </FormControl>
                    <FormControl mt={4} isInvalid={!!errors.full_name}>
                        <FormLabel htmlFor="full_name">{getTranslation("form_label_full_name")}</FormLabel>
                        <Input
                            id="full_name"
                            {...register("full_name")}
                            placeholder={getTranslation("form_placeholder_full_name")}
                            type="text"
                        />
                        {errors.full_name && (
                            <FormErrorMessage>{errors.full_name.message}</FormErrorMessage>
                        )}
                    </FormControl>
                    <FormControl mt={4} isRequired isInvalid={!!errors.password}>
                        <FormLabel htmlFor="password">{getTranslation("form_label_set_password")}</FormLabel>
                        <Input
                            id="password"
                            {...register("password", {
                                required: getTranslation("form_validation_password_required"),
                                minLength: {
                                    value: 8,
                                    message: getTranslation("form_validation_password_min_length"),
                                },
                            })}
                            placeholder={getTranslation("form_placeholder_password")}
                            type="password"
                        />
                        {errors.password && (
                            <FormErrorMessage>{errors.password.message}</FormErrorMessage>
                        )}
                    </FormControl>
                    <FormControl mt={4} isRequired isInvalid={!!errors.confirm_password}>
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
                        <FormControl>
                            <Checkbox {...register("is_superuser")} colorScheme="teal">
                                {getTranslation("checkbox_is_admin")}
                            </Checkbox>
                        </FormControl>
                        <FormControl>
                            <Checkbox {...register("is_active")} colorScheme="teal">
                                {getTranslation("checkbox_is_active")}
                            </Checkbox>
                        </FormControl>
                    </Flex>
                </ModalBody>
                <ModalFooter gap={3}>
                    <Button variant="primary" type="submit" isLoading={isSubmitting}>
                        {getTranslation("button_save")}
                    </Button>
                    <Button onClick={onClose}>{getTranslation("button_cancel")}</Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
};

export default AddUser;
