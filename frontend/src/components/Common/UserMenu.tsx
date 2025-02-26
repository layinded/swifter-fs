import {
    Box,
    IconButton,
    Menu,
    MenuButton,
    MenuItem,
    MenuList,
} from "@chakra-ui/react";
import {Link} from "@tanstack/react-router";
import {FaUserAstronaut} from "react-icons/fa";
import {FiLogOut, FiUser} from "react-icons/fi";
import useAuth from "../../hooks/useAuth";
import {useTranslationHelper} from "../../utils/translationHelper";

const UserMenu = () => {
    const {logout} = useAuth();

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) return <p>Loading translations...</p>;

    const handleLogout = async () => {
        await logout();
    };

    return (
        <>
            {/* Desktop */}
            <Box display={{base: "none", md: "block"}} position="fixed" top={4} right={4}>
                <Menu>
                    <MenuButton
                        as={IconButton}
                        aria-label={getTranslation("user_menu_options")}
                        icon={<FaUserAstronaut color="white" fontSize="18px"/>}
                        bg="ui.main"
                        isRound
                        data-testid="user-menu"
                        _hover={{bg: "ui.secondary"}}
                    />
                    <MenuList>
                        <MenuItem icon={<FiUser fontSize="18px"/>} as={Link} to="/settings">
                            {getTranslation("user_menu_my_profile")}
                        </MenuItem>
                        <MenuItem
                            icon={<FiLogOut fontSize="18px"/>}
                            onClick={handleLogout}
                            color="ui.danger"
                            fontWeight="bold"
                        >
                            {getTranslation("user_menu_log_out")}
                        </MenuItem>
                    </MenuList>
                </Menu>
            </Box>
        </>
    );
};

export default UserMenu;
