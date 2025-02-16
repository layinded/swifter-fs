import {
  Button,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  useDisclosure,
} from "@chakra-ui/react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { FiEdit, FiTrash } from "react-icons/fi";

import type { UserPublic } from "../../client";
import EditUser from "../Admin/EditUser";
import Delete from "./DeleteAlert";

interface ActionsMenuProps {
  type: "User" | string;
  value: UserPublic;
  disabled?: boolean;
}

const ActionsMenu = ({ type, value, disabled }: ActionsMenuProps) => {
  const editModal = useDisclosure();
  const deleteModal = useDisclosure();

  return (
    <>
      <Menu>
        <MenuButton
          isDisabled={disabled}
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="unstyled"
        />
        <MenuList>
          <MenuItem onClick={editModal.onOpen} icon={<FiEdit fontSize="16px" />}>
            Edit {type}
          </MenuItem>
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="red.500"
          >
            Delete {type}
          </MenuItem>
        </MenuList>
        {type === "User" && (
          <EditUser user={value as UserPublic} isOpen={editModal.isOpen} onClose={editModal.onClose} />
        )}
        <Delete type={type} id={value.id} isOpen={deleteModal.isOpen} onClose={deleteModal.onClose} />
      </Menu>
    </>
  );
};

export default ActionsMenu;
