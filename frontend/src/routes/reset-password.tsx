import {
  Button,
  Container,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Text,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { createFileRoute, redirect, useNavigate } from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import { type ApiError } from "../client/core/ApiError";
import { AuthenticationService } from "../client/sdk.gen";
import { isLoggedIn } from "../hooks/useAuth";
import useCustomToast from "../hooks/useCustomToast";
import { confirmPasswordRules, handleError, passwordRules } from "../utils";

interface NewPasswordForm {
  new_password: string;
  confirm_password: string;
}

export const Route = createFileRoute("/reset-password")({
  component: ResetPassword,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({ to: "/" });
    }
  },
});

function ResetPassword() {
  const {
    register,
    handleSubmit,
    getValues,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<NewPasswordForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: { new_password: "" },
  });

  const showToast = useCustomToast();
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: async (data: { new_password: string }) => {
      const token = new URLSearchParams(window.location.search).get("token");
      if (!token) {
        throw new Error("Invalid or missing token.");
      }
      await AuthenticationService.authenticationResetPassword({
        requestBody: { new_password: data.new_password, token },
      });
    },
    onSuccess: () => {
      showToast("Success!", "Password updated successfully.", "success");
      reset();
      navigate({ to: "/login" });
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
  });

  const onSubmit: SubmitHandler<NewPasswordForm> = async (data) => {
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
        Reset Password
      </Heading>
      <Text textAlign="center">
        Please enter your new password and confirm it to reset your password.
      </Text>
      <FormControl mt={4} isInvalid={!!errors.new_password}>
        <FormLabel htmlFor="password">New Password</FormLabel>
        <Input
          id="password"
          {...register("new_password", passwordRules())}
          placeholder="Enter new password"
          type="password"
        />
        {errors.new_password && (
          <FormErrorMessage>{errors.new_password.message}</FormErrorMessage>
        )}
      </FormControl>
      <FormControl mt={4} isInvalid={!!errors.confirm_password}>
        <FormLabel htmlFor="confirm_password">Confirm Password</FormLabel>
        <Input
          id="confirm_password"
          {...register("confirm_password", confirmPasswordRules(getValues))}
          placeholder="Confirm new password"
          type="password"
        />
        {errors.confirm_password && (
          <FormErrorMessage>{errors.confirm_password.message}</FormErrorMessage>
        )}
      </FormControl>
      <Button
        variant="primary"
        type="submit"
        isLoading={isSubmitting}
        isDisabled={isSubmitting}
      >
        Reset Password
      </Button>
    </Container>
  );
}

export default ResetPassword;
