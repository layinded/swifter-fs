import {Button, Flex, Text} from "@chakra-ui/react";
import {useTranslationHelper} from "../../utils/translationHelper";

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
    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <Text>Loading translations...</Text>;
    }

    // Replace placeholder in the pagination page label if needed.
    const pageLabel = getTranslation("pagination_page").replace("{page}", page.toString());

    return (
        <Flex gap={4} alignItems="center" mt={4} direction="row" justifyContent="center">
            <Button
                onClick={() => onChangePage(page - 1)}
                isDisabled={!hasPreviousPage || page <= 1}
                colorScheme="teal"
                variant="outline"
            >
                {getTranslation("pagination_previous")}
            </Button>
            <Text fontWeight="bold">{pageLabel}</Text>
            <Button
                isDisabled={!hasNextPage}
                onClick={() => onChangePage(page + 1)}
                colorScheme="teal"
                variant="outline"
            >
                {getTranslation("pagination_next")}
            </Button>
        </Flex>
    );
}
