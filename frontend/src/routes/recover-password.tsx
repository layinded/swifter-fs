import {
  Button,
  Container,
  FormControl,
  FormErrorMessage,
  Heading,
  Input,
  Text,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { createFileRoute, redirect } from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import { type ApiError } from "../client/core/ApiError";
import { AuthenticationService } from "../client/sdk.gen"; // ✅ Fixed Import
import { isLoggedIn } from "../hooks/useAuth";
import useCustomToast from "../hooks/useCustomToast";
import { emailPattern, handleError } from "../utils";

interface FormData {
  email: string;
}

export const Route = createFileRoute("/recover-password")({
  component: RecoverPassword,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({ to: "/" });
    }
  },
});

function RecoverPassword() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormData>();

  const showToast = useCustomToast();

  const mutation = useMutation({
    mutationFn: async (data: FormData) => {
      await AuthenticationService.authenticationRecoverPassword(data); // ✅ Fixed Service Call
    },
    onSuccess: () => {
      showToast(
        "Email sent.",
        "We sent an email with a link to reset your password.",
        "success"
      );
      reset();
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
  });

  const onSubmit: SubmitHandler<FormData> = async (data) => {
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
        Password Recovery
      </Heading>
      <Text align="center">
        Enter your registered email, and we will send you a password reset link.
      </Text>
      <FormControl isInvalid={!!errors.email}>
        <Input
          id="email"
          {...register("email", {
            required: "Email is required",
            pattern: emailPattern,
          })}
          placeholder="Enter your email"
          type="email"
        />
        {errors.email && (
          <FormErrorMessage>{errors.email.message}</FormErrorMessage>
        )}
      </FormControl>
      <Button
        variant="primary"
        type="submit"
        isLoading={isSubmitting}
        isDisabled={isSubmitting} // ✅ Disabled Button While Submitting
      >
        Send Reset Link
      </Button>
    </Container>
  );
}

export default RecoverPassword;
