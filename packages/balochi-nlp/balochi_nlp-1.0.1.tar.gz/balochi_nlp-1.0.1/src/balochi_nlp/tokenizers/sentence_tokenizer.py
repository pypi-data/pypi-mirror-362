import re
from typing import List


class BalochiSentenceTokenizer:
    """A sentence tokenizer specifically designed for the Balochi language."""

    def __init__(self):
        # Sentence ending punctuation marks in Balochi
        self.sentence_endings = r"[.!?؟]+"

        # Abbreviations and special cases that don't end sentences
        self.abbreviations = ["ڈاکٹر", "پروف", "محترم", "جناب"]

        # Compile the abbreviations pattern
        self.abbrev_pattern = "|".join(map(re.escape, self.abbreviations))

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Balochi text into sentences.

        Args:
            text (str): Input text in Balochi

        Returns:
            List[str]: List of sentences
        """
        # Clean the text
        text = text.strip()

        # Handle abbreviations by temporarily replacing periods
        for abbrev in self.abbreviations:
            text = text.replace(f"{abbrev}.", f"{abbrev}@PERIOD@")

        # Split on sentence endings
        potential_sentences = re.split(self.sentence_endings, text)

        # Process sentences
        sentences = []
        for sent in potential_sentences:
            # Restore periods in abbreviations
            sent = sent.replace("@PERIOD@", ".")

            # Clean and add to results
            sent = sent.strip()
            if sent:
                sentences.append(sent)

        return sentences

    def tokenize_with_boundaries(self, text: str) -> List[dict]:
        """
        Tokenize text into sentences and preserve boundary information.

        Args:
            text (str): Input text in Balochi

        Returns:
            List[dict]: List of dictionaries containing sentence information
        """
        sentences = []
        start = 0

        # Find all potential sentence boundaries
        for match in re.finditer(self.sentence_endings, text):
            end = match.end()

            # Get the sentence and its ending punctuation
            sentence = text[start:end].strip()
            if sentence:
                # Check if the sentence ends with an abbreviation
                is_abbrev = any(
                    sentence.endswith(abbrev + ".") for abbrev in self.abbreviations
                )

                if not is_abbrev:
                    sentences.append(
                        {
                            "text": sentence,
                            "start": start,
                            "end": end,
                            "ending": match.group(),
                        }
                    )
                    start = end

        # Add the last sentence if there is one
        if start < len(text):
            last_sentence = text[start:].strip()
            if last_sentence:
                sentences.append(
                    {
                        "text": last_sentence,
                        "start": start,
                        "end": len(text),
                        "ending": "",
                    }
                )

        return sentences
