import {
    AlertDialog,
    AlertDialogBody,
    AlertDialogContent,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogOverlay,
    Button,
} from "@chakra-ui/react";
import {useMutation, useQueryClient} from "@tanstack/react-query";
import React from "react";
import {useForm} from "react-hook-form";

import {AdminService} from "../../client";
import useCustomToast from "../../hooks/useCustomToast";
import {useTranslationHelper} from "../../utils/translationHelper";

interface DeleteProps {
    type: "User" | string;
    id: string;
    isOpen: boolean;
    onClose: () => void;
}

const Delete = ({type, id, isOpen, onClose}: DeleteProps) => {
    const queryClient = useQueryClient();
    const showToast = useCustomToast();
    const cancelRef = React.useRef<HTMLButtonElement | null>(null);

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) return <p>Loading translations...</p>;

    // Use the provided type to build dynamic text
    const entity = type.toLowerCase();
    const headerText = getTranslation("delete_alert_header").replace("{type}", type);
    const userWarning =
        type === "User" ? getTranslation("delete_alert_user_warning") + " " : "";
    const confirmationText = getTranslation("delete_alert_confirmation");
    const fullBodyText = userWarning + confirmationText;

    const mutation = useMutation({
        mutationFn: async () => {
            if (type === "User") {
                await AdminService.deleteUser({userId: id});
            } else {
                console.error(`Unexpected entity type: ${type}`);
                throw new Error(`Deletion not implemented for ${type}`);
            }
        },
        onSuccess: () => {
            showToast(
                getTranslation("delete_success_title"),
                getTranslation("delete_success_message").replace("{entity}", entity),
                "success"
            );
            onClose();
            queryClient.invalidateQueries({
                queryKey: type === "User" ? ["users"] : [entity],
            });
        },
        onError: () => {
            showToast(
                getTranslation("delete_error_title"),
                getTranslation("delete_error_message").replace("{entity}", entity),
                "error"
            );
        },
    });

    const {handleSubmit, formState: {isSubmitting}} = useForm();

    const onSubmit = async () => {
        mutation.mutate();
    };

    return (
        <AlertDialog
            isOpen={isOpen}
            onClose={onClose}
            leastDestructiveRef={cancelRef}
            size={{base: "sm", md: "md"}}
            isCentered
        >
            <AlertDialogOverlay>
                <AlertDialogContent as="form" onSubmit={handleSubmit(onSubmit)}>
                    <AlertDialogHeader>{headerText}</AlertDialogHeader>
                    <AlertDialogBody>{fullBodyText}</AlertDialogBody>
                    <AlertDialogFooter gap={3}>
                        <Button colorScheme="red" type="submit" isLoading={isSubmitting}>
                            {getTranslation("delete_button")}
                        </Button>
                        <Button ref={cancelRef} onClick={onClose} isDisabled={isSubmitting}>
                            {getTranslation("cancel_button")}
                        </Button>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialogOverlay>
        </AlertDialog>
    );
};

export default Delete;
