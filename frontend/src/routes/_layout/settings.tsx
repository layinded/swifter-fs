import {
    Container,
    Heading,
    Tab,
    TabList,
    TabPanel,
    TabPanels,
    Tabs,
} from "@chakra-ui/react";
import {createFileRoute} from "@tanstack/react-router";
import useAuth from "../../hooks/useAuth";
import {useTranslationHelper} from "../../utils/translationHelper";

import Appearance from "../../components/UserSettings/Appearance";
import ChangePassword from "../../components/UserSettings/ChangePassword";
import DeleteAccount from "../../components/UserSettings/DeleteAccount";
import UserInformation from "../../components/UserSettings/UserInformation";

const tabsConfig = [
    {title: "My Profile", key: "settings_my_profile", component: UserInformation},
    {title: "Password", key: "settings_password", component: ChangePassword},
    {title: "Appearance", key: "settings_appearance", component: Appearance},
    {title: "Danger Zone", key: "settings_danger_zone", component: DeleteAccount},
];

export const Route = createFileRoute("/_layout/settings")({
    component: UserSettings,
});

function UserSettings() {
    const {user} = useAuth();
    const currentUser = user; // Assuming user is returned from useAuth

    // Use our centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    if (isTranslationsLoading) {
        return <p>Loading translations...</p>;
    }

    // For non-admin users, omit the Danger Zone tab.
    const finalTabs = (currentUser?.is_superuser ? tabsConfig : tabsConfig.slice(0, 3)).map(
        (tab) => ({
            ...tab,
            title: getTranslation(tab.key),
        })
    );

    return (
        <Container maxW="full">
            <Heading size="lg" textAlign={{base: "center", md: "left"}} pt={12}>
                {getTranslation("settings_user_settings")}
            </Heading>
            <Tabs variant="enclosed">
                <TabList>
                    {finalTabs.map((tab, index) => (
                        <Tab key={index}>{tab.title}</Tab>
                    ))}
                </TabList>
                <TabPanels>
                    {finalTabs.map(({component: Component}, index) => (
                        <TabPanel key={index}>
                            <Component/> {/* Render the tab content component */}
                        </TabPanel>
                    ))}
                </TabPanels>
            </Tabs>
        </Container>
    );
}

export default UserSettings;
