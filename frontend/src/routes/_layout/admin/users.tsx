import {
    Box,
    Badge,
    Container,
    Flex,
    Heading,
    SkeletonText,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
} from "@chakra-ui/react";
import {useQuery, useQueryClient} from "@tanstack/react-query";
import {createFileRoute, useNavigate} from "@tanstack/react-router";
import {useEffect} from "react";
import {z} from "zod";


import type {UserPublic, GetAllUsersResponse} from "../../../client";
import {AdminService} from "../../../client";
import AddUser from "../../../components/Admin/AddUser";
import ActionsMenu from "../../../components/Common/ActionsMenu";
import Navbar from "../../../components/Common/Navbar";
import {PaginationFooter} from "../../../components/Common/PaginationFooter";
import useAuth from "../../../hooks/useAuth";
import {useTranslationHelper} from "../../../utils/translationHelper";

// Validate search params with Zod.
const usersSearchSchema = z.object({
    page: z.number().catch(1),
});

export const Route = createFileRoute("/_layout/admin/users")({
    component: Admin,
    validateSearch: (search) => usersSearchSchema.parse(search),
});

const PER_PAGE = 5;

function getUsersQueryOptions({page}: { page: number }) {
    return {
        queryFn: async (): Promise<GetAllUsersResponse> =>
            AdminService.getAllUsers({skip: (page - 1) * PER_PAGE, limit: PER_PAGE}),
        queryKey: ["users", {page}],
    };
}

function UsersTable({
                        getTranslation,
                    }: {
    getTranslation: (key: string, replacements?: Record<string, string>) => string;
}) {
    const queryClient = useQueryClient();
    const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"]);
    const {page} = Route.useSearch();
    const navigate = useNavigate({from: Route.fullPath});

    const setPage = (page: number) =>
        navigate({
            search: (prev: Record<string, any>) => ({...prev, page}),
        });

    const {data: users, isPending, isPlaceholderData} = useQuery({
        ...getUsersQueryOptions({page}),
        placeholderData: (prevData) => prevData,
    });

    const hasNextPage = !isPlaceholderData && users?.data.length === PER_PAGE;
    const hasPreviousPage = page > 1;

    useEffect(() => {
        if (hasNextPage) {
            queryClient.prefetchQuery(getUsersQueryOptions({page: page + 1}));
        }
    }, [page, queryClient, hasNextPage]);

    return (
        <>
            <TableContainer>
                <Table size={{base: "sm", md: "md"}}>
                    <Thead>
                        <Tr>
                            <Th width="20%">{getTranslation("admin_full_name")}</Th>
                            <Th width="50%">{getTranslation("admin_email")}</Th>
                            <Th width="10%">{getTranslation("admin_role")}</Th>
                            <Th width="10%">{getTranslation("admin_status")}</Th>
                            <Th width="10%">{getTranslation("admin_actions")}</Th>
                        </Tr>
                    </Thead>
                    {isPending ? (
                        <Tbody>
                            <Tr>
                                {new Array(5).fill(null).map((_, index) => (
                                    <Td key={index}>
                                        <SkeletonText noOfLines={1} paddingBlock="16px"/>
                                    </Td>
                                ))}
                            </Tr>
                        </Tbody>
                    ) : (
                        <Tbody>
                            {users?.data.map((user: UserPublic) => (
                                <Tr key={user.id}>
                                    <Td color={!user.full_name ? "ui.dim" : "inherit"} isTruncated maxWidth="150px">
                                        {user.full_name || getTranslation("admin_na")}
                                        {currentUser?.id === user.id && (
                                            <Badge ml="1" colorScheme="teal">
                                                {getTranslation("admin_you")}
                                            </Badge>
                                        )}
                                    </Td>
                                    <Td isTruncated maxWidth="150px">
                                        {user.email}
                                    </Td>
                                    <Td>
                                        {user.is_superuser
                                            ? getTranslation("admin_admin")
                                            : getTranslation("admin_user")}
                                    </Td>
                                    <Td>
                                        <Flex gap={2}>
                                            <Box
                                                w="2"
                                                h="2"
                                                borderRadius="50%"
                                                bg={user.is_active ? "ui.success" : "ui.danger"}
                                                alignSelf="center"
                                            />
                                            {user.is_active
                                                ? getTranslation("admin_active")
                                                : getTranslation("admin_inactive")}
                                        </Flex>
                                    </Td>
                                    <Td>
                                        <ActionsMenu
                                            type="User"
                                            value={user}
                                            disabled={currentUser?.id === user.id}
                                        />
                                    </Td>
                                </Tr>
                            ))}
                        </Tbody>
                    )}
                </Table>
            </TableContainer>
            <PaginationFooter
                onChangePage={setPage}
                page={page}
                hasNextPage={hasNextPage}
                hasPreviousPage={hasPreviousPage}
            />
        </>
    );
}

function Admin() {
    useAuth();
    // Use the centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    return (
        <Container maxW="full">
            <Heading size="lg" textAlign={{base: "center", md: "left"}} pt={12}>
                {getTranslation("admin_users_management")}
            </Heading>
            <Navbar type="User" addModalAs={AddUser}/>
            <UsersTable getTranslation={getTranslation}/>
        </Container>
    );
}

export default Admin;
