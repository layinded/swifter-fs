import {
  Badge,
  Container,
  Heading,
  Radio,
  RadioGroup,
  Stack,
  useColorMode,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";

const Appearance = () => {
  const { colorMode, setColorMode } = useColorMode();
  const [selectedMode, setSelectedMode] = useState<string>(colorMode);

  useEffect(() => {
    if (selectedMode === "light" || selectedMode === "dark") {
      setColorMode(selectedMode);
    }
  }, [selectedMode, setColorMode]);

  return (
    <Container maxW="full">
      <Heading size="sm" py={4}>
        Appearance
      </Heading>
      <RadioGroup onChange={(value) => setSelectedMode(value)} value={selectedMode}>
        <Stack>
          <Radio value="light" colorScheme="teal">
            Light Mode
            {colorMode === "light" && (
              <Badge ml="1" colorScheme="teal">
                Default
              </Badge>
            )}
          </Radio>
          <Radio value="dark" colorScheme="teal">
            Dark Mode
          </Radio>
          <Radio value="system" colorScheme="teal">
            System Default
          </Radio>
        </Stack>
      </RadioGroup>
    </Container>
  );
};

export default Appearance;
