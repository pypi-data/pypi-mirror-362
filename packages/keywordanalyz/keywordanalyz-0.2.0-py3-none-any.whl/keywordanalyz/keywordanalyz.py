import yake
from lingua import Language, LanguageDetectorBuilder


class TextAnalyser:
    def __init__(
        self,
        allowed_languages: list[Language] = [
            Language.ENGLISH,
            Language.FRENCH,
            Language.GERMAN,
            Language.SPANISH,
        ],
        maximum_keywords: int = 10,
        max_n_gram_size: int = 3,
    ):
        """Initialise the TextAnalyser
        About max_n_gram_size: This controls, as I understand it, the number of words per keyword. Lower it and you get shorter keywords, raise it and you get longer keywords.
        """
        self.allowed_languages = allowed_languages
        self.maximum_keywords = maximum_keywords
        self.max_n_gram_size = max_n_gram_size
        self.language_detector = LanguageDetectorBuilder.from_languages(
            *allowed_languages
        ).build()

        # Create one keyword extractor per allowed langauge
        self.keyword_extractors = {}
        for language in allowed_languages:
            self.keyword_extractors[language.iso_code_639_1.name.lower()] = (
                yake.KeywordExtractor(
                    top=self.maximum_keywords,
                    lan=language.iso_code_639_1.name.lower(),
                    n=max_n_gram_size,
                )
            )

    def _get_language_of_text(self, text: str):
        """Get the language of the input text
        This function uses lingua to calculate the language of the input text.
        """

        # Get the language possibilites
        text_language = self.language_detector.compute_language_confidence_values(text)

        # Convert them all to a tuple with lowercase language name and float with number in it
        compiled_text_language = []
        for language in text_language:
            compiled_text_language.append(
                (language.language.iso_code_639_1.name.lower(), float(language.value))
            )

        return compiled_text_language

    def _get_keywords_from_text(self, text: str, language: str):
        keyword_extractor = self.keyword_extractors[language]
        extracted_keywords = keyword_extractor.extract_keywords(text)
        compiled_keywords = []

        for keyword in extracted_keywords:
            compiled_keywords.append((keyword[0], float(keyword[1])))

        return compiled_keywords

    def analyse(self, text: str, language: str | None = None, verbose: bool = False):
        # Check if the input language is a string or None
        if language is None:
            # If None, then check the language with lingua
            text_languages = self._get_language_of_text(text)
            if text_languages is not None:
                language = text_languages[0][0]
            else:
                # If the outputted language is also None (no language detected), set to english as default
                langauge = "en"
        else:
            # If input language is not None, convert the string to lowercase and set text_languages
            language = language.lower()
            text_languages = [(language, 1.0)]

        keywords = self._get_keywords_from_text(text, language)

        if verbose == True:
            return {
                "language": language,
                "raw_langauges": text_languages,
                "keywords": keywords,
            }
        else:
            return {"language": language, "keywords": keywords}
