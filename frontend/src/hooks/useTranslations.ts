import {useQuery} from "@tanstack/react-query";
import {LanguagesService} from "../client";

// Optional: define the shape of each translation record from the server
type TranslationItem = {
    key: string;
    value: string;
};

const useTranslations = (language: string) => {
    return useQuery<Record<string, string>, Error>({
        queryKey: ["translations", language],
        queryFn: async () => {
            const response: TranslationItem[] = await LanguagesService.getTranslations({
                languageCode: language,
            });
            // Convert [{ key, value }, ...] => { [key]: value, ... }
            return response.reduce((acc, {key, value}) => {
                acc[key] = value;
                return acc;
            }, {} as Record<string, string>);
        },
        // Remove cacheTime if it causes TS errors
        // cacheTime: Infinity,
        staleTime: Infinity,
        refetchOnWindowFocus: false,
    });
};

export default useTranslations;
