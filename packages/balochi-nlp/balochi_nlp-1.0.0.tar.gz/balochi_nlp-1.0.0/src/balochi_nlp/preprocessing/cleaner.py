import re


class BalochiTextCleaner:
    """Text cleaner for Balochi language."""

    def __init__(self):
        # Regular expressions for cleaning
        self.url_pattern = r"https?://\S+|www\.\S+"
        self.email_pattern = r"\S+@\S+\.\S+"
        self.number_pattern = r"\d+"
        self.emoji_pattern = (
            r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
            r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]"
        )

        # Non-Balochi script patterns
        self.latin_pattern = r"[a-zA-Z]+"
        self.chinese_pattern = r"[\u4e00-\u9fff]+"
        self.devanagari_pattern = r"[\u0900-\u097F]+"

        # Extra spaces and newlines
        self.extra_spaces = r"\s+"
        self.extra_newlines = r"\n\s*\n"

        # Special Balochi characters
        self.special_chars = ["ءُ", "ءَ", "ءِ"]

    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return re.sub(self.url_pattern, " ", text)

    def remove_emails(self, text: str) -> str:
        """Remove email addresses from text."""
        return re.sub(self.email_pattern, " ", text)

    def remove_numbers(self, text: str) -> str:
        """Remove numbers from text."""
        return re.sub(self.number_pattern, " ", text)

    def remove_emojis(self, text: str) -> str:
        """Remove emojis from text."""
        return re.sub(self.emoji_pattern, " ", text)

    def remove_non_balochi(self, text: str) -> str:
        """Remove non-Balochi script characters."""
        text = re.sub(self.latin_pattern, " ", text)
        text = re.sub(self.chinese_pattern, " ", text)
        text = re.sub(self.devanagari_pattern, " ", text)
        return text

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace and newlines."""
        # Replace multiple spaces with single space
        text = re.sub(self.extra_spaces, " ", text)
        # Replace multiple newlines with single newline
        text = re.sub(self.extra_newlines, "\n", text)
        return text.strip()

    def process_special_chars(self, text: str) -> str:
        """
        Process text with special handling for Balochi characters.
        Particularly handles the 'ء' character and its combinations.
        """
        processed_tokens = []
        for token in text.split():
            if "ء" in token:
                # Handle special cases like 'ءُ', 'ءَ', 'ءِ' being attached to words
                if "ءُ" in token:
                    parts = token.split("ءُ")
                    for part in parts:
                        if part:
                            processed_tokens.append(part)
                    processed_tokens.append("ءُ")
                elif "ءَ" in token:
                    parts = token.split("ءَ")
                    for part in parts:
                        if part:
                            processed_tokens.append(part)
                    processed_tokens.append("ءَ")
                elif "ءِ" in token:
                    parts = token.split("ءِ")
                    for part in parts:
                        if part:
                            processed_tokens.append(part)
                    processed_tokens.append("ءِ")
                else:
                    # For other cases, split around 'ء'
                    parts = re.split(r"(ء)", token)
                    for part in parts:
                        if part:  # Avoid empty strings
                            processed_tokens.append(part)
            else:
                processed_tokens.append(token)
        return " ".join(processed_tokens)

    def clean_text(
        self,
        text: str,
        remove_numbers: bool = True,
        preserve_special_chars: bool = True,
    ) -> str:
        """
        Comprehensive text cleaning that combines all cleaning operations and
        properly handles Balochi special characters.

        Args:
            text (str): Input text to clean
            remove_numbers (bool): Whether to remove numbers from text
            preserve_special_chars (bool): Whether to preserve and handle special
                Balochi characters

        Returns:
            str: Cleaned text
        """
        # Initial cleaning
        text = text.strip()

        # Remove unwanted elements
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.remove_emojis(text)

        if preserve_special_chars:
            # Remove unwanted characters while preserving special Balochi characters
            text = re.sub(r"[^\w\sءُءَءِ،؛٫.!?؟]", "", text)
        else:
            # Remove all non-word characters
            text = re.sub(r"[^\w\s]", "", text)

        # Remove English letters and other non-Balochi scripts
        text = self.remove_non_balochi(text)

        # Remove numbers if requested
        if remove_numbers:
            text = self.remove_numbers(text)

        # Normalize whitespace
        text = self.normalize_whitespace(text)

        # Handle special Balochi characters if requested
        if preserve_special_chars:
            text = self.process_special_chars(text)

        return text.strip()

    def clean_file(self, file_path: str, **kwargs) -> str:
        """
        Read a file and clean its contents.

        Args:
            file_path (str): Path to the file to clean
            **kwargs: Additional arguments to pass to clean_text

        Returns:
            str: Cleaned text
        """
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return self.clean_text(text, **kwargs)
