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

import { AdminService } from "../../client/sdk.gen";
import useCustomToast from "../../hooks/useCustomToast";

interface DeleteProps {
  type: "User" | string;
  id: string;
  isOpen: boolean;
  onClose: () => void;
}

const Delete = ({ type, id, isOpen, onClose }: DeleteProps) => {
  const queryClient = useQueryClient();
  const showToast = useCustomToast();
  const cancelRef = React.useRef<HTMLButtonElement | null>(null);

  const { handleSubmit, formState: { isSubmitting } } = useForm();

  const deleteEntity = async () => {
    try {
      if (type === "User") {
        await AdminService.deleteUser({ userId: id });
      } else {
        console.error(`Unexpected entity type: ${type}`);
        throw new Error(`Deletion not implemented for ${type}`);
      }
    } catch (error) {
      console.error("Deletion error:", error);
      throw new Error(`Failed to delete ${type.toLowerCase()}`);
    }
  };

  const mutation = useMutation({
    mutationFn: deleteEntity,
    onSuccess: () => {
      showToast("Success", `The ${type.toLowerCase()} was deleted successfully.`, "success");
      onClose();
      queryClient.invalidateQueries({ queryKey: type === "User" ? ["users"] : [type.toLowerCase()] });
    },
    onError: () => {
      showToast("An error occurred.", `Failed to delete the ${type.toLowerCase()}.`, "error");
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
          <AlertDialogHeader>Delete {type}</AlertDialogHeader>

          <AlertDialogBody>
            {type === "User" && (
              <span>
                All items associated with this user will also be
                <strong> permanently deleted. </strong>
              </span>
            )}
            Are you sure? This action cannot be undone.
          </AlertDialogBody>

          <AlertDialogFooter gap={3}>
            <Button colorScheme="red" type="submit" isLoading={isSubmitting}>
              Delete
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

export default Delete;
