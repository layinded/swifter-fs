import {useMutation, useQuery, useQueryClient, UseQueryOptions} from "@tanstack/react-query";
import {useNavigate} from "@tanstack/react-router";
import {useState} from "react";
import {AxiosError} from "axios";
import {AuthenticationService} from "../client";
import type {
    AuthenticationLoginUserData as AccessToken,
    AuthenticationLoginUserResponse,
    UserPublic,
    RegisterNewUserData as UserRegister,
} from "../client/types.gen";

import useCustomToast from "./useCustomToast";

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
        // Use placeholderData so that data is always defined
        placeholderData: {google: null, facebook: null, github: null},
        // onError is not recognized by the raw type so we force it
        onError: (error: unknown) => {
            console.error("Failed to fetch OAuth URLs:", error);
            showToast("OAuth Error", "Failed to load social login URLs.", "error");
        },
    } as unknown as UseQueryOptions<
        { google?: string | null; facebook?: string | null; github?: string | null },
        Error,
        { google?: string | null; facebook?: string | null; github?: string | null },
        readonly ["oauthUrls"]
    >;

    const {data: oauthUrlsData} = useQuery(oauthQueryOptions);
    const oauthUrls = oauthUrlsData ?? {google: null, facebook: null, github: null};


    const logout = async () => {
        try {
            const refreshToken = localStorage.getItem("refresh_token");
            if (refreshToken) {
                await AuthenticationService.authenticationLogout({
                    requestBody: {refresh_token: refreshToken},
                });
            }
        } catch (error: any) {
            // If it's a 401 error, we can assume the token is already invalid
            if (error.response?.status === 401) {
                console.warn("Token already revoked or invalid; proceeding with logout.");
            } else {
                console.error("Logout API call failed:", error);
            }
        }

        // Clear tokens and update state regardless of the API call result
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        queryClient.setQueryData(["currentUser"], null);
        navigate({to: "/login"});
        showToast("Logged Out", "You have been logged out successfully.", "info");
    };

    const {data: user, isLoading} = useQuery<UserPublic | null, AxiosError>({
        queryKey: ["currentUser"],
        queryFn: async () => {
            try {
                return await AuthenticationService.getCurrentUser();
            } catch (err) {
                if (err instanceof AxiosError && err.response?.status === 401) {
                    logout();
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

    const signUpMutation = useMutation({
        mutationFn: async (data: UserRegister) =>
            AuthenticationService.registerNewUser({...data}),
        onSuccess: () => {
            navigate({to: "/login"});
            showToast("Account Created", "Your account has been successfully created.", "success");
        },
        onError: (err: unknown) => {
            let errDetail = "An error occurred";
            if (err instanceof AxiosError) {
                errDetail = err.response?.data?.message?.details ?? err.message;
            } else {
                errDetail = "User already exists."
            }
            showToast("Signup Failed", errDetail, "error");
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
            showToast("Welcome!", "You have logged in successfully.", "success");
        },
        onError: (err: unknown) => {
            let errDetail = "Invalid credentials";
            if (err instanceof AxiosError) {
                errDetail = err.response?.data?.message ?? err.message;
            }
            setError(errDetail);
            showToast("Login Failed", errDetail, "error");
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
