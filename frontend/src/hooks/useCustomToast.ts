// src/hooks/useCustomToast.ts
import { useToast } from "@chakra-ui/react";
import { useCallback } from "react";

const useCustomToast = () => {
  const toast = useToast();

  const showToast = useCallback(
    (
      title: string,
      description: string,
      status: "success" | "error" | "warning" | "info"
    ) => {
      toast({
        title,
        description,
        status,
        duration: 5000,
        isClosable: true,
        position: "bottom-right",
        variant: "subtle",
      });
    },
    [toast]
  );

  return showToast;
};

export default useCustomToast;
