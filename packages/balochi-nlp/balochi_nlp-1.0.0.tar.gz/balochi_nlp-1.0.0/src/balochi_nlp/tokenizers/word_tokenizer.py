import re
from typing import List, TypedDict


class TokenInfo(TypedDict):
    """Type definition for token information dictionary."""

    token: str
    prefixes: List[str]
    suffixes: List[str]


class BalochiWordTokenizer:
    """A word tokenizer specifically designed for the Balochi language."""

    def __init__(self):
        # Common Balochi word boundaries and punctuation
        self.word_boundaries = r'[\s,.!?؟،:;"\']+'
        # Common Balochi prefixes and suffixes
        self.prefixes = ["بے", "نا", "بی"]
        self.suffixes = ["ان", "ئے", "ئا", "ئی"]

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Balochi text into words.

        Args:
            text (str): Input text in Balochi

        Returns:
            List[str]: List of tokenized words
        """
        # Clean the text
        text = text.strip()

        # Split on word boundaries
        tokens = re.split(self.word_boundaries, text)

        # Remove empty tokens
        tokens = [token for token in tokens if token]

        # Handle special cases (compound words, affixes)
        processed_tokens: List[str] = []
        for token in tokens:
            # Check for compound words (words connected with zero-width non-joiner)
            if "\u200c" in token:
                parts = token.split("\u200c")
                processed_tokens.extend(parts)
            else:
                processed_tokens.append(token)

        return processed_tokens

    def tokenize_with_affixes(self, text: str) -> List[TokenInfo]:
        """
        Tokenize text and identify prefixes and suffixes.

        Args:
            text (str): Input text in Balochi

        Returns:
            List[TokenInfo]: List of dictionaries with token information
        """
        tokens = self.tokenize(text)
        result: List[TokenInfo] = []

        for token in tokens:
            token_info: TokenInfo = {
                "token": token,
                "prefixes": [],
                "suffixes": [],
            }

            # Check for prefixes
            for prefix in self.prefixes:
                if token.startswith(prefix):
                    token_info["prefixes"].append(prefix)

            # Check for suffixes
            for suffix in self.suffixes:
                if token.endswith(suffix):
                    token_info["suffixes"].append(suffix)

            result.append(token_info)

        return result
