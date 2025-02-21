import {
    Box,
    Flex,
    Icon,
    Text,
    useColorModeValue,
} from "@chakra-ui/react";
import {useQueryClient} from "@tanstack/react-query";
import {Link} from "@tanstack/react-router";
import {FiHome, FiSettings, FiUsers, FiGlobe} from "react-icons/fi";
import type {UserPublic} from "../../client/types.gen";
import {useTranslationHelper} from "../../utils/translationHelper";

interface SidebarItemsProps {
    onClose?: () => void;
}

const SidebarItems = ({onClose}: SidebarItemsProps) => {
    const queryClient = useQueryClient();
    const textColor = useColorModeValue("ui.main", "ui.light");
    const bgActive = useColorModeValue("#E2E8F0", "#4A5568");

    const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"]);

    // Define base menu items with translation keys.
    const baseItems = [
        {icon: FiHome, titleKey: "sidebar_dashboard", path: "/"},
        {icon: FiSettings, titleKey: "sidebar_user_settings", path: "/settings"},
    ];

    // Define admin-only items.
    const adminItems = [
        {icon: FiUsers, titleKey: "sidebar_admin", path: "/admin/users"},
        {icon: FiGlobe, titleKey: "sidebar_translations", path: "/admin/translations"},
    ];

    // If the current user is admin, include adminItems.
    const finalItems = currentUser?.is_superuser
        ? [...baseItems, ...adminItems]
        : baseItems;

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <Box>Loading translations...</Box>;
    }

    const listItems = finalItems.map(({icon, titleKey, path}) => (
        <Flex
            as={Link}
            to={path}
            w="100%"
            p={2}
            key={titleKey}
            activeProps={{
                style: {
                    background: bgActive,
                    borderRadius: "12px",
                },
            }}
            color={textColor}
            onClick={onClose}
        >
            <Icon as={icon} alignSelf="center"/>
            <Text ml={2}>{getTranslation(titleKey)}</Text>
        </Flex>
    ));

    return <Box>{listItems}</Box>;
};

export default SidebarItems;
