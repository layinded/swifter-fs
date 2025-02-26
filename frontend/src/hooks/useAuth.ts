import {useMutation, useQuery, useQueryClient, UseQueryOptions} from "@tanstack/react-query";
import {useNavigate} from "@tanstack/react-router";
import {useState} from "react";
import {AxiosError} from "axios";
import {AuthenticationService} from "../client";
import type {
    AuthenticationLoginUserData as AccessToken,
    AuthenticationLoginUserResponse,
    RegisterNewUserData as UserRegister,
    UserPublic,
} from "../client/types.gen";

import useCustomToast from "./useCustomToast";
import useTranslations from "./useTranslations";

const isLoggedIn = () => {
    const token = localStorage.getItem("access_token");
    if (!token) return false;
    try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        return payload.exp * 1000 > Date.now();
    } catch (error) {
        return false;
    }
};

const useAuth = () => {
    const apiUrl = import.meta.env.VITE_API_URL;
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();
    const showToast = useCustomToast();
    const queryClient = useQueryClient();

    // Determine the language:
    // If the current user is loaded and has a preferred language, use that.
    // Otherwise, check localStorage or default to "en".
    const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"]);
    const langFromUser = currentUser?.preferred_language;
    const storedLang = localStorage.getItem("preferred_language");
    const language = langFromUser || storedLang || "en";

    // Load translations based on the determined language.

    // @ts-ignore
    const {data: translationsData, isLoading: isTranslationsLoading} = useTranslations(language);
    const translations = translationsData ?? {};
    const getTranslation = (key: string): string => translations[key] || key;

    // Fetch OAuth URLs using React Query
    const oauthQueryOptions = {
        queryKey: ["oauthUrls"] as const,
        queryFn: async () => {
            const response = await fetch(apiUrl + "/api/v1/oauth/urls");
            if (!response.ok) {
                throw new Error("Failed to fetch OAuth URLs");
            }
            return await response.json();
        },
        enabled: Boolean(apiUrl),
        staleTime: 1000 * 60 * 5,
        placeholderData: {google: null, facebook: null, github: null},
        onError: (error: unknown) => {
            console.error("Failed to fetch OAuth URLs:", error);
            showToast(
                getTranslation("oauth_error"),
                getTranslation("oauth_error_message"),
                "error"
            );
        },
    } as unknown as UseQueryOptions<
        { google?: string | null; facebook?: string | null; github?: string | null },
        Error,
        { google?: string | null; facebook?: string | null; github?: string | null },
        readonly ["oauthUrls"]
    >;

    const {data: oauthUrlsData} = useQuery(oauthQueryOptions);
    const oauthUrls = oauthUrlsData ?? {google: null, facebook: null, github: null};

    // Fetch user data
    const {data: user, isLoading} = useQuery<UserPublic | null, AxiosError>({
        queryKey: ["currentUser"],
        queryFn: async () => {
            try {
                return await AuthenticationService.getCurrentUser();
            } catch (err) {
                if (err instanceof AxiosError && err.response?.status === 401) {
                    await logout();
                }
                throw err;
            }
        },
        enabled: isLoggedIn(),
        staleTime: 1000 * 60 * 5,
        refetchOnWindowFocus: false,
        retry: false,
        select: (data) => data ?? null,
    });

    const logout = async () => {
        try {
            const refreshToken = localStorage.getItem("refresh_token");
            if (refreshToken) {
                await AuthenticationService.authenticationLogout({
                    requestBody: {refresh_token: refreshToken},
                });
            }
        } catch (error: any) {
            if (error.response?.status === 401) {
                console.warn("Token already revoked or invalid; proceeding with logout.");
            } else {
                console.error("Logout API call failed:", error);
            }
        }
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        queryClient.setQueryData(["currentUser"], null);
        navigate({to: "/login"});
        showToast(
            getTranslation("logged_out"),
            getTranslation("logged_out_successfully"),
            "info"
        );
    };

    const signUpMutation = useMutation({
        mutationFn: async (data: UserRegister) =>
            AuthenticationService.registerNewUser({...data}),
        onSuccess: () => {
            navigate({to: "/login"});
            showToast(
                getTranslation("account_created"),
                getTranslation("account_created_message"),
                "success"
            );
        },
        onError: (err: unknown) => {
            let errDetail = "An error occurred";
            if (err instanceof AxiosError) {
                errDetail = err.response?.data?.message?.details ?? err.message;
            } else {
                errDetail = getTranslation("user_already_exists") || "User already exists.";
            }
            showToast(
                getTranslation("signup_failed"),
                errDetail,
                "error"
            );
        },
        onSettled: () => {
            queryClient.invalidateQueries({queryKey: ["users"]});
        },
    });

    const loginMutation = useMutation({
        mutationFn: async (data: AccessToken) => {
            const response: AuthenticationLoginUserResponse =
                await AuthenticationService.authenticationLoginUser({
                    formData: data.formData,
                });
            localStorage.setItem("access_token", response.access_token);
            localStorage.setItem("refresh_token", response.refresh_token ?? "");
            const userProfile = await AuthenticationService.getCurrentUser();
            queryClient.setQueryData(["currentUser"], userProfile);
        },
        onSuccess: () => {
            navigate({to: "/"});
            showToast(
                getTranslation("welcome"),
                getTranslation("login_success"),
                "success"
            );
        },
        onError: (err: unknown) => {
            let errDetail = "Invalid credentials";
            if (err instanceof AxiosError) {
                errDetail = err.response?.data?.message ?? err.message;
            }
            setError(errDetail);
            showToast(
                getTranslation("login_failed"),
                errDetail,
                "error"
            );
        },
    });

    return {
        signUpMutation,
        loginMutation,
        logout,
        user,
        isLoading,
        oauthUrls,
        error,
        resetError: () => setError(null),
    };
};

export {isLoggedIn};
export default useAuth;
