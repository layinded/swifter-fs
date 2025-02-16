// src/components/common/PaginationFooter.tsx
import { Button, Flex, Text } from "@chakra-ui/react";

type PaginationFooterProps = {
  hasNextPage?: boolean;
  hasPreviousPage?: boolean;
  onChangePage: (newPage: number) => void;
  page: number;
};

export function PaginationFooter({
  hasNextPage,
  hasPreviousPage,
  onChangePage,
  page,
}: PaginationFooterProps) {
  return (
    <Flex
      gap={4}
      alignItems="center"
      mt={4}
      direction="row"
      justifyContent="center"
    >
      <Button
        onClick={() => onChangePage(page - 1)}
        isDisabled={!hasPreviousPage || page <= 1}
        colorScheme="teal"
        variant="outline"
      >
        Previous
      </Button>
      <Text fontWeight="bold">Page {page}</Text>
      <Button
        isDisabled={!hasNextPage}
        onClick={() => onChangePage(page + 1)}
        colorScheme="teal"
        variant="outline"
      >
        Next
      </Button>
    </Flex>
  );
}
