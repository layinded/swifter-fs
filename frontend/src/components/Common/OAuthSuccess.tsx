import {useEffect, useRef} from "react";
import {useNavigate} from "@tanstack/react-router";
import useCustomToast from "../../hooks/useCustomToast";
import {processOAuthTokens} from "../../utils";
import {useTranslationHelper} from "../../utils/translationHelper";

const OAuthSuccess = () => {
    const navigate = useNavigate();
    const showToast = useCustomToast();
    const hasProcessedRef = useRef(false);

    // Use the centralized translation helper.
    const {getTranslation, isTranslationsLoading} = useTranslationHelper();

    useEffect(() => {
        // Wait until translations are loaded.
        if (isTranslationsLoading) return;
        // Guard against double execution (e.g. in React StrictMode)
        if (hasProcessedRef.current) return;
        hasProcessedRef.current = true;

        const tokens = processOAuthTokens();
        if (tokens) {
            navigate({to: "/"});
            showToast(
                getTranslation("oauth_success_welcome"),
                getTranslation("oauth_success_message"),
                "success"
            );
        } else {
            showToast(
                getTranslation("oauth_error_title"),
                getTranslation("oauth_error_message"),
                "error"
            );
            setTimeout(() => {
                navigate({to: "/login?error=missing_tokens"});
            }, 1000); // Delay to allow the toast to show
        }
    }, [isTranslationsLoading, navigate, showToast, getTranslation]);

    return <p>{getTranslation("oauth_processing")}</p>;
};

export default OAuthSuccess;
