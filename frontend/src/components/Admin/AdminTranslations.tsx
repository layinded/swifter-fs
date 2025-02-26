// src/components/Admin/AdminTranslations.tsx
import {
    Box,
    Button,
    Container,
    FormControl,
    FormLabel,
    Heading,
    Input,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
    Text,
    useToast,
    useDisclosure,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalCloseButton,
    ModalBody,
    ModalFooter,
} from "@chakra-ui/react";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {useState} from "react";
import {useForm} from "react-hook-form";
import {useTranslationHelper} from "../../utils/translationHelper";
import {LanguagesService} from "../../client";
import useAuth from "../../hooks/useAuth";
// Import generated types from your OpenAPI SDK
import type {TranslationCreate, TranslationPublic, TranslationUpdate} from "../../client";

function AdminTranslations() {
    // Unconditionally call all hooks.
    const queryClient = useQueryClient();
    const toast = useToast();
    const {user} = useAuth();
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    const {data: translationsBulk, isLoading} = useQuery({
        queryKey: ["translations", "bulk"],
        queryFn: async () =>
            LanguagesService.getBulkTranslations({languages: ["en", "cs"]}),
    });

    const {
        register: registerNew,
        handleSubmit: handleSubmitNew,
        reset: resetNewForm,
        formState: {errors: newFormErrors},
    } = useForm<TranslationCreate>();

    const {
        register: registerEdit,
        handleSubmit: handleSubmitEdit,
        reset: resetEditForm,
        formState: {errors: editFormErrors},
    } = useForm<TranslationUpdate>();

    const {isOpen: isEditOpen, onOpen: onEditOpen, onClose: onEditClose} = useDisclosure();
    const {isOpen: isDeleteOpen, onOpen: onDeleteOpen, onClose: onDeleteClose} = useDisclosure();

    const [filter, setFilter] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;
    const [selectedEditTranslation, setSelectedEditTranslation] = useState<TranslationPublic | null>(null);
    const [selectedDeleteTranslation, setSelectedDeleteTranslation] = useState<TranslationPublic | null>(null);

    const createMutation = useMutation({
        mutationFn: async (data: { requestBody: TranslationCreate }) =>
            LanguagesService.createTranslation(data),
        onSuccess: () => {
            toast({
                title: getTranslation("translation_created"),
                description: getTranslation("translation_created_successfully"),
                status: "success",
                duration: 3000,
                isClosable: true,
            });
            queryClient.invalidateQueries({queryKey: ["translations", "bulk"]});
            resetNewForm();
        },
        onError: (error: any) => {
            toast({
                title: getTranslation("translation_create_error"),
                description: JSON.stringify(error),
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        },
    });

    const updateMutation = useMutation({
        mutationFn: async (data: { translationId: string; requestBody: TranslationUpdate }) =>
            LanguagesService.updateTranslation(data),
        onSuccess: () => {
            toast({
                title: getTranslation("translation_updated"),
                description: getTranslation("translation_updated_successfully"),
                status: "success",
                duration: 3000,
                isClosable: true,
            });
            queryClient.invalidateQueries({queryKey: ["translations", "bulk"]});
            onEditClose();
            setSelectedEditTranslation(null);
            resetEditForm();
        },
        onError: (error: any) => {
            toast({
                title: getTranslation("translation_update_error"),
                description: JSON.stringify(error),
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        },
    });

    const deleteMutation = useMutation({

        mutationFn: async (data: { translationId: string }) =>
            LanguagesService.deleteTranslation(data),

        onSuccess: () => {
            toast({
                title: getTranslation("translation_deleted"),
                description: getTranslation("translation_deleted_successfully"),
                status: "success",
                duration: 3000,
                isClosable: true,
            });
            queryClient.invalidateQueries({queryKey: ["translations", "bulk"]});
            onDeleteClose();
            setSelectedDeleteTranslation(null);
        },
        onError: (error: any) => {
            toast({
                title: getTranslation("translation_delete_error"),
                description: JSON.stringify(error),
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        },
    });

    // Now conditionally render based on user.
    if (!user) {
        return <p>{getTranslation("loading_translations")}</p>;
    }
    if (!user.is_superuser) {
        return <Text>{getTranslation("admin_translations_access_denied")}</Text>;
    }
    if (isTranslationsLoading || isLoading) {
        return <p>{getTranslation("loading_translations")}</p>;
    }

    const bulkTranslationsData = translationsBulk || {};

    // Flatten translations from the bulk endpoint.
    const allTranslations: { language_code: string; id: string; value: string; key: string }[] =
        Object.entries(bulkTranslationsData).flatMap(([lang, transObj]) =>
            Object.entries(transObj as Record<string, string>).map(([key, value]) => ({
                language_code: lang,
                key,
                value,
                id: `${lang}-${key}`, // Note: this composite id may not be valid for deletion!
            }))
        );

    const filteredTranslations = allTranslations.filter((item) => {
        const lang = item.language_code || "";
        const key = item.key || "";
        const value = item.value || "";
        return (
            lang.toLowerCase().includes(filter.toLowerCase()) ||
            key.toLowerCase().includes(filter.toLowerCase()) ||
            value.toLowerCase().includes(filter.toLowerCase())
        );
    });

    const totalPages = Math.ceil(filteredTranslations.length / itemsPerPage);
    const paginatedTranslations = filteredTranslations.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    const renderRows = () =>
        paginatedTranslations.map((item) => (
            <Tr key={item.id}>
                <Td>{item.language_code}</Td>
                <Td>{item.key}</Td>
                <Td>{item.value}</Td>
                <Td>
                    <Button
                        size="sm"
                        colorScheme="blue"
                        mr={2}
                        onClick={() => {
                            setSelectedEditTranslation(item);
                            resetEditForm({value: item.value});
                            onEditOpen();
                        }}
                    >
                        {getTranslation("translation_edit")}
                    </Button>
                    <Button
                        size="sm"
                        colorScheme="red"
                        onClick={() => {
                            setSelectedDeleteTranslation(item);
                            onDeleteOpen();
                        }}
                    >
                        {getTranslation("translation_delete")}
                    </Button>
                </Td>
            </Tr>
        ));

    const onSubmitNew = (data: TranslationCreate) => {
        console.log("Creating translation with:", data);
        createMutation.mutate({requestBody: data});
    };

    const onSubmitEdit = (data: TranslationUpdate) => {
        if (selectedEditTranslation) {
            updateMutation.mutate({
                translationId: selectedEditTranslation.id,
                requestBody: data,
            });
        }
    };

    return (
        <Container maxW="full" py={4}>
            <Heading mb={4}>{getTranslation("admin_translations_heading")}</Heading>

            {/* Create New Translation Form */}
            <Box as="form" onSubmit={handleSubmitNew(onSubmitNew)} mb={6} borderWidth={1} borderRadius="md" p={4}>
                <Heading size="md" mb={2}>
                    {getTranslation("translation_create_heading")}
                </Heading>
                <FormControl mb={2} isInvalid={!!newFormErrors.language_code}>
                    <FormLabel>{getTranslation("translation_language_code")}</FormLabel>
                    <Input
                        placeholder={getTranslation("translation_language_code_placeholder")}
                        {...registerNew("language_code", {required: true, maxLength: 5})}
                    />
                    {newFormErrors.language_code && <Text color="red.500">{getTranslation("required_field")}</Text>}
                </FormControl>
                <FormControl mb={2} isInvalid={!!newFormErrors.key}>
                    <FormLabel>{getTranslation("translation_key")}</FormLabel>
                    <Input
                        placeholder={getTranslation("translation_key_placeholder")}
                        {...registerNew("key", {required: true, maxLength: 255})}
                    />
                    {newFormErrors.key && <Text color="red.500">{getTranslation("required_field")}</Text>}
                </FormControl>
                <FormControl mb={2} isInvalid={!!newFormErrors.value}>
                    <FormLabel>{getTranslation("translation_value")}</FormLabel>
                    <Input
                        placeholder={getTranslation("translation_value_placeholder")}
                        {...registerNew("value", {required: true, maxLength: 1000})}
                    />
                    {newFormErrors.value && <Text color="red.500">{getTranslation("required_field")}</Text>}
                </FormControl>
                <Button type="submit">{getTranslation("translation_create_button")}</Button>
            </Box>

            {/* Filter Input */}
            <Box mb={4}>
                <Input
                    placeholder={getTranslation("translation_filter_placeholder")}
                    value={filter}
                    onChange={(e) => {
                        setFilter(e.target.value);
                        setCurrentPage(1);
                    }}
                />
            </Box>

            {/* Translations Table */}
            <TableContainer>
                <Table variant="simple">
                    <Thead>
                        <Tr>
                            <Th>{getTranslation("translation_language_code")}</Th>
                            <Th>{getTranslation("translation_key")}</Th>
                            <Th>{getTranslation("translation_value")}</Th>
                            <Th>{getTranslation("translation_actions")}</Th>
                        </Tr>
                    </Thead>
                    <Tbody>{renderRows()}</Tbody>
                </Table>
            </TableContainer>

            {/* Pagination Controls */}
            <Box mt={4} display="flex" justifyContent="center" alignItems="center">
                <Button
                    mr={2}
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                >
                    {getTranslation("pagination_previous")}
                </Button>
                <Text>
                    {currentPage} / {totalPages || 1}
                </Text>
                <Button
                    ml={2}
                    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages || totalPages === 0}
                >
                    {getTranslation("pagination_next")}
                </Button>
            </Box>

            {/* Edit Translation Modal */}
            <Modal isOpen={isEditOpen} onClose={onEditClose}>
                <ModalOverlay/>
                <ModalContent>
                    <ModalHeader>{getTranslation("translation_edit_heading")}</ModalHeader>
                    <ModalCloseButton/>
                    <ModalBody>
                        <Box as="form" id="editForm" onSubmit={handleSubmitEdit(onSubmitEdit)}>
                            <FormControl mb={2}>
                                <FormLabel>{getTranslation("translation_language_code")}</FormLabel>
                                <Input value={selectedEditTranslation?.language_code || ""} isReadOnly/>
                            </FormControl>
                            <FormControl mb={2}>
                                <FormLabel>{getTranslation("translation_key")}</FormLabel>
                                <Input value={selectedEditTranslation?.key || ""} isReadOnly/>
                            </FormControl>
                            <FormControl mb={2} isInvalid={!!editFormErrors.value}>
                                <FormLabel>{getTranslation("translation_value")}</FormLabel>
                                <Input
                                    placeholder={getTranslation("translation_value_placeholder")}
                                    {...registerEdit("value", {required: true, maxLength: 1000})}
                                />
                                {editFormErrors.value &&
                                    <Text color="red.500">{getTranslation("required_field")}</Text>}
                            </FormControl>
                        </Box>
                    </ModalBody>
                    <ModalFooter>
                        <Button variant="ghost" mr={3} onClick={onEditClose}>
                            {getTranslation("cancel")}
                        </Button>
                        <Button type="submit" form="editForm" colorScheme="blue">
                            {getTranslation("save")}
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>

            {/* Delete Translation Modal */}
            <Modal isOpen={isDeleteOpen} onClose={onDeleteClose}>
                <ModalOverlay/>
                <ModalContent>
                    <ModalHeader>{getTranslation("translation_delete_heading")}</ModalHeader>
                    <ModalCloseButton/>
                    <ModalBody>
                        <Text>{getTranslation("translation_delete_confirmation")}</Text>
                    </ModalBody>
                    <ModalFooter>
                        <Button variant="ghost" mr={3} onClick={onDeleteClose}>
                            {getTranslation("cancel")}
                        </Button>
                        <Button
                            colorScheme="red"
                            onClick={() => {
                                if (selectedDeleteTranslation) {
                                    deleteMutation.mutate({translationId: selectedDeleteTranslation.id});
                                }
                            }}
                        >
                            {getTranslation("delete")}
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </Container>
    );
}

export default AdminTranslations;
