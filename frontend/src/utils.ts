import type {ApiError} from "./client"

export const emailPattern = {
    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
    // Use a translation key instead of a hardcoded message.
    message: "form_invalid_email_address",
}

export const namePattern = {
    value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
    message: "form_invalid_name",
}

export const passwordRules = (isRequired = true) => {
    const rules: any = {
        minLength: {
            value: 8,
            message: "form_password_min_length",
        },
    }

    if (isRequired) {
        rules.required = "form_password_required"
    }

    return rules
}

export const confirmPasswordRules = (
    getValues: () => any,
    isRequired = true,
) => {
    const rules: any = {
        validate: (value: string) => {
            const password = getValues().password || getValues().new_password
            return value === password ? true : "form_passwords_do_not_match"
        },
    }

    if (isRequired) {
        rules.required = "form_password_confirmation_required"
    }

    return rules
}

export const handleError = (err: ApiError, showToast: any) => {
    const errDetail = (err.body as any)?.detail
    let errorMessage = errDetail || "form_generic_error"
    if (Array.isArray(errDetail) && errDetail.length > 0) {
        errorMessage = errDetail[0].msg
    }
    // Use the key "error" as the title for the toast.
    showToast("error", errorMessage, "error")
}

export const processOAuthTokens = (): { accessToken: string; refreshToken: string } | null => {
    const params = new URLSearchParams(window.location.search)
    const accessToken = params.get("access_token")
    const refreshToken = params.get("refresh_token")

    if (accessToken && refreshToken) {
        localStorage.setItem("access_token", accessToken)
        localStorage.setItem("refresh_token", refreshToken)
        return {accessToken, refreshToken}
    } else {
        console.error("oauth_tokens_missing_error")
        return null
    }
}
