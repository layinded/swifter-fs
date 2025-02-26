import {
    Button,
    Menu,
    MenuButton,
    MenuItem,
    MenuList,
    useDisclosure,
} from "@chakra-ui/react";
import {BsThreeDotsVertical} from "react-icons/bs";
import {FiEdit, FiTrash} from "react-icons/fi";

import type {UserPublic} from "../../client";
import EditUser from "../Admin/EditUser";
import Delete from "./DeleteAlert";
import {useTranslationHelper} from "../../utils/translationHelper";

interface ActionsMenuProps {
    type: "User" | string;
    value: UserPublic;
    disabled?: boolean;
}

const ActionsMenu = ({type, value, disabled}: ActionsMenuProps) => {
    const editModal = useDisclosure();
    const deleteModal = useDisclosure();

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    // Prepare labels using translation keys.
    const editText = `${getTranslation("actions_menu_edit")} ${type}`;
    const deleteText = `${getTranslation("actions_menu_delete")} ${type}`;

    return (
        <>
            <Menu>
                <MenuButton
                    isDisabled={disabled}
                    as={Button}
                    rightIcon={<BsThreeDotsVertical/>}
                    variant="unstyled"
                />
                <MenuList>
                    <MenuItem onClick={editModal.onOpen} icon={<FiEdit fontSize="16px"/>}>
                        {editText}
                    </MenuItem>
                    <MenuItem
                        onClick={deleteModal.onOpen}
                        icon={<FiTrash fontSize="16px"/>}
                        color="red.500"
                    >
                        {deleteText}
                    </MenuItem>
                </MenuList>
                {type === "User" && (
                    <EditUser
                        user={value as UserPublic}
                        isOpen={editModal.isOpen}
                        onClose={editModal.onClose}
                    />
                )}
                <Delete
                    type={type}
                    id={value.id}
                    isOpen={deleteModal.isOpen}
                    onClose={deleteModal.onClose}
                />
            </Menu>
        </>
    );
};

export default ActionsMenu;
