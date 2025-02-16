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
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, useEffect } from "react";
import { type SubmitHandler, useForm } from "react-hook-form";

import { type UserUpdateMe } from "../../client"; // ✅ Fixed Import
import { UsersService } from "../../client";
import type { ApiError } from "../../client";
import useAuth from "../../hooks/useAuth";
import useCustomToast from "../../hooks/useCustomToast";
import { emailPattern, handleError } from "../../utils";

const UserInformation = () => {
  const queryClient = useQueryClient();
  const color = useColorModeValue("inherit", "ui.light");
  const showToast = useCustomToast();
  const [editMode, setEditMode] = useState(false);
  const { user: currentUser } = useAuth();

  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { isSubmitting, errors, isDirty },
  } = useForm<UserUpdateMe>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      full_name: currentUser?.full_name || "",
      email: currentUser?.email || "",
    },
  });

  // Update form values when currentUser changes
  useEffect(() => {
    reset({
      full_name: currentUser?.full_name || "",
      email: currentUser?.email || "",
    });
  }, [currentUser, reset]);

  const toggleEditMode = () => {
    setEditMode(!editMode);
  };

  const mutation = useMutation({
    mutationFn: (data: UserUpdateMe) =>
      UsersService.updateCurrentUser({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "User information updated successfully.", "success");
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
      setEditMode(false);
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
  });

  const onSubmit: SubmitHandler<UserUpdateMe> = async (data) => {
    mutation.mutate(data);
  };

  const onCancel = () => {
    reset();
    toggleEditMode();
  };

  return (
    <Container maxW="full">
      <Heading size="sm" py={4}>
        User Information
      </Heading>
      <Box w={{ sm: "full", md: "50%" }} as="form" onSubmit={handleSubmit(onSubmit)}>
        <FormControl>
          <FormLabel color={color} htmlFor="full_name">
            Full Name
          </FormLabel>
          {editMode ? (
            <Input
              id="full_name"
              {...register("full_name", { maxLength: 30 })}
              type="text"
              size="md"
              w="auto"
            />
          ) : (
            <Text size="md" py={2} color={!currentUser?.full_name ? "ui.dim" : "inherit"}>
              {currentUser?.full_name || "N/A"}
            </Text>
          )}
        </FormControl>
        <FormControl mt={4} isInvalid={!!errors.email}>
          <FormLabel color={color} htmlFor="email">
            Email
          </FormLabel>
          {editMode ? (
            <Input
              id="email"
              {...register("email", {
                required: "Email is required",
                pattern: emailPattern,
              })}
              type="email"
              size="md"
              w="auto"
            />
          ) : (
            <Text size="md" py={2} isTruncated>
              {currentUser?.email}
            </Text>
          )}
          {errors.email && <FormErrorMessage>{errors.email.message}</FormErrorMessage>}
        </FormControl>
        <Flex mt={4} gap={3}>
          <Button
            variant="primary"
            onClick={!editMode ? toggleEditMode : undefined}
            type={editMode ? "submit" : "button"}
            isLoading={editMode ? isSubmitting : false}
            isDisabled={editMode ? !isDirty || !getValues("email") : false}
          >
            {editMode ? "Save" : "Edit"}
          </Button>
          {editMode && (
            <Button onClick={onCancel} isDisabled={isSubmitting}>
              Cancel
            </Button>
          )}
        </Flex>
      </Box>
    </Container>
  );
};

export default UserInformation;
