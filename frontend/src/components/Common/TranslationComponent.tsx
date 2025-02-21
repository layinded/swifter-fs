import useTranslations from "../../hooks/useTranslations";
import useAuth from "../../hooks/useAuth";

const TranslationComponent = ({ textKey }: { textKey: string }) => {
  // Get user data and its loading state from useAuth
  const { user, isLoading: authLoading } = useAuth();

  // Wait for user data to load so we know the preferred language
  if (authLoading) return <p>Loading user data...</p>;

  // Use the user's preferred language if available, otherwise default to "en"
  const language = user?.preferred_language || "en";

  // Call the translations hook with the determined language
  // When `language` changes, the query key ["translations", language] changes,
  // prompting React Query to fetch the appropriate translations.
  const { data: translations, isLoading, error } = useTranslations(language);

  if (isLoading) return <p>Loading translations...</p>;
  if (error) return <p>Error loading translations</p>;

  // Retrieve the translated text using the provided textKey
  const translatedText = translations?.[textKey] || textKey;

  return <p>{translatedText}</p>;
};

export default TranslationComponent;
