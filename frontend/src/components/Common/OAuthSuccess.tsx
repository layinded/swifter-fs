// src/components/Common/OAuthSuccess.tsx

import {useEffect, useRef} from "react";
import {useNavigate} from "@tanstack/react-router";
import useCustomToast from "../../hooks/useCustomToast";
import {processOAuthTokens} from "../../utils";

const OAuthSuccess = () => {
    const navigate = useNavigate();
    const showToast = useCustomToast();
    const hasProcessedRef = useRef(false);

    useEffect(() => {
        // Guard against double execution (e.g. in React StrictMode)
        if (hasProcessedRef.current) return;
        hasProcessedRef.current = true;

        const tokens = processOAuthTokens();
        if (tokens) {
            // Tokens exist, proceed immediately.
            navigate({to: "/"});
            showToast("Welcome!", "You have logged in successfully.", "success");
        } else {
            // Show error toast first and delay navigation slightly
            showToast("⚠️ Error", "Failed to log in. Please try again.", "error");
            setTimeout(() => {
                navigate({to: "/login?error=missing_tokens"});
            }, 1000); // 1-second delay to allow the toast to show
        }
    }, [navigate, showToast]);

    return <p>Processing login... Please wait.</p>;
};

export default OAuthSuccess;
