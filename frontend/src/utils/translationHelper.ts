// src/utils/translationHelper.ts
import useTranslations from "../hooks/useTranslations";
import useAuth from "../hooks/useAuth";

/**
 * A custom hook that returns:
 * - getTranslation: A function to retrieve the translation for a given key.
 *   If replacements are provided, it replaces placeholders in the translation.
 * - language: The current language (derived from the user context or a fallback).
 * - isTranslationsLoading: Whether the translations are still loading.
 * - translations: The loaded translations object.
 */
export const useTranslationHelper = () => {
    const {user} = useAuth();

    const defaultLang = "en";
    // Use the user’s preferred language if available; otherwise fallback to "en"
    const language = user?.preferred_language || defaultLang;
    const {data: translations, isLoading: isTranslationsLoading} = useTranslations(language);

    const getTranslation = (key: string, replacements?: Record<string, string>): string => {
        const base = translations?.[key] || key;
        if (replacements) {
            let result = base;
            Object.entries(replacements).forEach(([placeholder, value]) => {
                // Replace all occurrences of {placeholder} with the given value.
                result = result.replace(new RegExp(`{${placeholder}}`, "g"), value);
            });
            return result;
        }
        return base;
    };

    return {getTranslation, language, isTranslationsLoading, translations};
};
