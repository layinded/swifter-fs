import {
    Box,
    Button,
    Container,
    Flex,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Heading,
    Input,
    Select,
    Text,
    useColorModeValue,
} from "@chakra-ui/react";
import {useMutation, useQueryClient} from "@tanstack/react-query";
import {useState, useEffect} from "react";
import {type SubmitHandler, useForm} from "react-hook-form";

import {type UserUpdateMe} from "../../client";
import {UsersService} from "../../client";
import type {ApiError} from "../../client";
import useAuth from "../../hooks/useAuth";
import useCustomToast from "../../hooks/useCustomToast";
import {emailPattern, handleError} from "../../utils";
import {useTranslationHelper} from "../../utils/translationHelper";

interface UserUpdateMeExtended extends UserUpdateMe {
    preferred_language: string;
}

const UserInformation = () => {
    const queryClient = useQueryClient();
    const color = useColorModeValue("inherit", "ui.light");
    const showToast = useCustomToast();
    const [editMode, setEditMode] = useState(false);
    const {user: currentUser} = useAuth();

    // Use our centralized translation helper.
    const {getTranslation, language, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    const {
        register,
        handleSubmit,
        reset,
        getValues,
        formState: {isSubmitting, errors, isDirty},
    } = useForm<UserUpdateMeExtended>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            full_name: currentUser?.full_name || "",
            email: currentUser?.email || "",
            preferred_language: currentUser?.preferred_language || language,
        },
    });

    // Update form values when currentUser changes.
    useEffect(() => {
        reset({
            full_name: currentUser?.full_name || "",
            email: currentUser?.email || "",
            preferred_language: currentUser?.preferred_language || language,
        });
    }, [currentUser, reset, language]);

    const toggleEditMode = () => {
        setEditMode(!editMode);
    };

    const mutation = useMutation({
        mutationFn: (data: UserUpdateMeExtended) =>
            UsersService.updateCurrentUser({requestBody: data}),
        onSuccess: () => {
            // Update localStorage with the new preferred language if needed.
            const newLang = getValues("preferred_language");
            // Optionally, you can update your auth context here
            localStorage.setItem("preferred_language", newLang);
            showToast(
                getTranslation("success"),
                getTranslation("user_information_update_success"),
                "success"
            );
            queryClient.invalidateQueries({queryKey: ["currentUser"]});
            setEditMode(false);
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
    });

    const onSubmit: SubmitHandler<UserUpdateMeExtended> = async (data) => {
        mutation.mutate(data);
    };

    const onCancel = () => {
        reset();
        toggleEditMode();
    };

    return (
        <Container maxW="full">
            <Heading size="sm" py={4}>
                {getTranslation("user_information_heading")}
            </Heading>
            <Box
                w={{sm: "full", md: "50%"}}
                as="form"
                onSubmit={handleSubmit(onSubmit)}
            >
                <FormControl>
                    <FormLabel color={color} htmlFor="full_name">
                        {getTranslation("form_label_full_name")}
                    </FormLabel>
                    {editMode ? (
                        <Input
                            id="full_name"
                            {...register("full_name", {maxLength: 30})}
                            type="text"
                            size="md"
                            w="auto"
                        />
                    ) : (
                        <Text
                            size="md"
                            py={2}
                            color={!currentUser?.full_name ? "ui.dim" : "inherit"}
                        >
                            {currentUser?.full_name || getTranslation("form_text_na")}
                        </Text>
                    )}
                </FormControl>
                <FormControl mt={4} isInvalid={!!errors.email}>
                    <FormLabel color={color} htmlFor="email">
                        {getTranslation("form_label_email")}
                    </FormLabel>
                    {editMode ? (
                        <Input
                            id="email"
                            {...register("email", {
                                required: getTranslation("form_validation_email_required"),
                                pattern: emailPattern,
                            })}
                            type="email"
                            size="md"
                            w="auto"
                            placeholder={getTranslation("form_placeholder_email")}
                        />
                    ) : (
                        <Text size="md" py={2} isTruncated>
                            {currentUser?.email}
                        </Text>
                    )}
                    {errors.email && (
                        <FormErrorMessage>{errors.email.message}</FormErrorMessage>
                    )}
                </FormControl>
                {/* New field for Preferred Language */}
                <FormControl mt={4}>
                    <FormLabel color={color} htmlFor="preferred_language">
                        {getTranslation("form_label_preferred_language")}
                    </FormLabel>
                    {editMode ? (
                        <Select id="preferred_language" {...register("preferred_language")}>
                            <option value="en">{getTranslation("language_english")}</option>
                            <option value="cs">{getTranslation("language_czech")}</option>
                            {/* Add other language options as needed */}
                        </Select>
                    ) : (
                        <Text size="md" py={2}>
                            {currentUser?.preferred_language || getTranslation("form_text_na")}
                        </Text>
                    )}
                </FormControl>
                <Flex mt={4} gap={3}>
                    <Button
                        variant="primary"
                        onClick={!editMode ? toggleEditMode : undefined}
                        type={editMode ? "submit" : "button"}
                        isLoading={editMode ? isSubmitting : false}
                        isDisabled={editMode ? !isDirty || !getValues("email") : false}
                    >
                        {editMode
                            ? getTranslation("button_save")
                            : getTranslation("button_edit")}
                    </Button>
                    {editMode && (
                        <Button onClick={onCancel} isDisabled={isSubmitting}>
                            {getTranslation("button_cancel")}
                        </Button>
                    )}
                </Flex>
            </Box>
        </Container>
    );
};

export default UserInformation;
