class BalochiTextNormalizer:
    """Text normalizer for Balochi language."""

    def __init__(self):
        # Character normalization mappings
        self.char_maps = {
            # Normalize different forms of letters
            "ي": "ی",
            "ئ": "ی",
            "ك": "ک",
            "ة": "ہ",
            # Add more character mappings as needed
        }

        # Common diacritics in Balochi
        self.diacritics = [
            "\u064b",  # Fathatan
            "\u064c",  # Dammatan
            "\u064d",  # Kasratan
            "\u064e",  # Fatha
            "\u064f",  # Damma
            "\u0650",  # Kasra
            "\u0651",  # Shadda
            "\u0652",  # Sukun
        ]

    def normalize_chars(self, text: str) -> str:
        """
        Normalize characters according to the mapping.

        Args:
            text (str): Input text

        Returns:
            str: Normalized text
        """
        for original, normalized in self.char_maps.items():
            text = text.replace(original, normalized)
        return text

    def remove_diacritics(self, text: str) -> str:
        """
        Remove diacritical marks from text.

        Args:
            text (str): Input text

        Returns:
            str: Text without diacritics
        """
        for diacritic in self.diacritics:
            text = text.replace(diacritic, "")
        return text

    def normalize_spaces(self, text: str) -> str:
        """
        Normalize spaces in text.

        Args:
            text (str): Input text

        Returns:
            str: Text with normalized spaces
        """
        # Replace multiple spaces with single space
        text = " ".join(text.split())

        # Fix spacing around punctuation
        text = text.replace(" ،", "،")
        text = text.replace(" ؟", "؟")
        text = text.replace(" !", "!")
        text = text.replace(" .", ".")

        return text

    def normalize(self, text: str, remove_diacritics: bool = False) -> str:
        """
        Apply all normalization steps to the text.

        Args:
            text (str): Input text
            remove_diacritics (bool): Whether to remove diacritical marks

        Returns:
            str: Fully normalized text
        """
        # Character normalization
        text = self.normalize_chars(text)

        # Remove diacritics if requested
        if remove_diacritics:
            text = self.remove_diacritics(text)

        # Space normalization
        text = self.normalize_spaces(text)

        return text.strip()


def normalize_text(text):
    """
    Normalize the input text by converting it to lowercase and removing extra spaces.

    Args:
        text (str): The input text to normalize.

    Returns:
        str: The normalized text.
    """
    # Convert to lowercase
    normalized_text = text.lower()
    # Remove extra spaces
    normalized_text = " ".join(normalized_text.split())
    return normalized_text


def handle_diacritics(text):
    """
    Handle diacritics in the input text.

    Args:
        text (str): The input text to process.

    Returns:
        str: The text with diacritics handled.
    """
    # Example implementation (to be customized based on Balochi language specifics)
    # This is a placeholder for actual diacritic handling logic
    return text.replace("َ", "a").replace("ِ", "i").replace("ُ", "u")


def normalize_corpus(corpus):
    """
    Normalize a corpus of text.

    Args:
        corpus (list of str): A list of text strings to normalize.

    Returns:
        list of str: A list of normalized text strings.
    """
    return [normalize_text(handle_diacritics(text)) for text in corpus]
