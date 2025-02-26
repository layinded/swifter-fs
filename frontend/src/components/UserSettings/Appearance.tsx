import {
    Badge,
    Container,
    Heading,
    Radio,
    RadioGroup,
    Stack,
    useColorMode,
} from "@chakra-ui/react";
import {useEffect, useState} from "react";
import {useTranslationHelper} from "../../utils/translationHelper";

const Appearance = () => {
    const {colorMode, setColorMode} = useColorMode();
    const [selectedMode, setSelectedMode] = useState<string>(colorMode);

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) return <p>Loading translations...</p>;

    useEffect(() => {
        // Also consider "system" for system default.
        if (selectedMode === "light" || selectedMode === "dark" || selectedMode === "system") {
            setColorMode(selectedMode);
        }
    }, [selectedMode, setColorMode]);

    return (
        <Container maxW="full">
            <Heading size="sm" py={4}>
                {getTranslation("appearance_heading")}
            </Heading>
            <RadioGroup onChange={setSelectedMode} value={selectedMode}>
                <Stack>
                    <Radio value="light" colorScheme="teal">
                        {getTranslation("appearance_light_mode")}
                        {colorMode === "light" && (
                            <Badge ml="1" colorScheme="teal">
                                {getTranslation("appearance_default_badge")}
                            </Badge>
                        )}
                    </Radio>
                    <Radio value="dark" colorScheme="teal">
                        {getTranslation("appearance_dark_mode")}
                    </Radio>
                    <Radio value="system" colorScheme="teal">
                        {getTranslation("appearance_system_default")}
                    </Radio>
                </Stack>
            </RadioGroup>
        </Container>
    );
};

export default Appearance;
