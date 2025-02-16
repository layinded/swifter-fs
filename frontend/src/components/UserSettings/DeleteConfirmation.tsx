import {
  AlertDialog,
  AlertDialogBody,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogOverlay,
  Button,
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import React from "react";
import { useForm } from "react-hook-form";

import {AuthenticationService} from "../../client/sdk.gen"; // ✅ Fixed API call
import type { ApiError } from "../../client/core/ApiError";
import useAuth from "../../hooks/useAuth";
import useCustomToast from "../../hooks/useCustomToast";
import { handleError } from "../../utils";

interface DeleteProps {
  isOpen: boolean;
  onClose: () => void;
}

const DeleteConfirmation = ({ isOpen, onClose }: DeleteProps) => {
  const queryClient = useQueryClient();
  const showToast = useCustomToast();
  const cancelRef = React.useRef<HTMLButtonElement | null>(null);
  const { logout } = useAuth();

  const {
    handleSubmit,
    formState: { isSubmitting },
  } = useForm();

  const mutation = useMutation({
    mutationFn: () => AuthenticationService.deleteCurrentUser(), // ✅ Fixed API call
    onSuccess: () => {
      showToast("Success", "Your account has been permanently deleted.", "success");
      logout();
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
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
      size={{ base: "sm", md: "md" }}
      isCentered
    >
      <AlertDialogOverlay>
        <AlertDialogContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <AlertDialogHeader>Confirm Account Deletion</AlertDialogHeader>

          <AlertDialogBody>
            Your account and all associated data will be <strong>permanently deleted.</strong> If you are sure,
            click <strong>"Confirm"</strong> to proceed. This action <strong>cannot be undone.</strong>
          </AlertDialogBody>

          <AlertDialogFooter gap={3}>
            <Button colorScheme="red" type="submit" isLoading={isSubmitting}>
              Confirm
            </Button>
            <Button ref={cancelRef} onClick={onClose} isDisabled={isSubmitting}>
              Cancel
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialogOverlay>
    </AlertDialog>
  );
};

export default DeleteConfirmation;
