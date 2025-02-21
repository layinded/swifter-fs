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

import {AuthenticationService} from "../../client/sdk.gen";
import type {ApiError} from "../../client";
import useAuth from "../../hooks/useAuth";
import useCustomToast from "../../hooks/useCustomToast";
import {handleError} from "../../utils";
import {useTranslationHelper} from "../../utils/translationHelper";

interface DeleteProps {
    isOpen: boolean;
    onClose: () => void;
}

const DeleteConfirmation = ({isOpen, onClose}: DeleteProps) => {
    const queryClient = useQueryClient();
    const showToast = useCustomToast();
    const cancelRef = React.useRef<HTMLButtonElement | null>(null);
    const {logout} = useAuth();

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) return <p>Loading translations...</p>;

    const {handleSubmit, formState: {isSubmitting}} = useForm();

    const mutation = useMutation({
        mutationFn: () => AuthenticationService.deleteCurrentUser(),
        onSuccess: () => {
            showToast(
                getTranslation("delete_account_success_title"),
                getTranslation("delete_account_success_message"),
                "success"
            );
            logout();
            queryClient.invalidateQueries({queryKey: ["currentUser"]});
            onClose();
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
    });

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
                    <AlertDialogHeader>
                        {getTranslation("delete_confirmation_header")}
                    </AlertDialogHeader>
                    <AlertDialogBody>
                        {getTranslation("delete_confirmation_body")}
                    </AlertDialogBody>
                    <AlertDialogFooter gap={3}>
                        <Button colorScheme="red" type="submit" isLoading={isSubmitting}>
                            {getTranslation("delete_confirmation_button_confirm")}
                        </Button>
                        <Button ref={cancelRef} onClick={onClose} isDisabled={isSubmitting}>
                            {getTranslation("delete_confirmation_button_cancel")}
                        </Button>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialogOverlay>
        </AlertDialog>
    );
};

export default DeleteConfirmation;
