import argparse
import json
import sys
from typing import Dict, Optional, Union

from balochi_nlp.preprocessing.cleaner import BalochiTextCleaner
from balochi_nlp.preprocessing.normalizer import BalochiTextNormalizer
from balochi_nlp.tokenizers.sentence_tokenizer import BalochiSentenceTokenizer
from balochi_nlp.tokenizers.word_tokenizer import BalochiWordTokenizer


def read_text_file(file_path: str) -> str:
    """Read text from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_output(
    output: Dict[str, Union[str, int, list]], output_file: Optional[str] = None
) -> None:
    """Write output to file or stdout."""
    output_json = json.dumps(output, ensure_ascii=False, indent=2)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_json)
    else:
        print(output_json)


def main() -> None:
    parser = argparse.ArgumentParser(description="Balochi NLP Tools")
    parser.add_argument("input_file", help="Input text file path")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument(
        "--task",
        "-t",
        required=True,
        choices=["tokenize-words", "tokenize-sentences", "clean", "normalize"],
        help="NLP task to perform",
    )

    # Task-specific arguments
    parser.add_argument(
        "--remove-urls", action="store_true", help="Remove URLs from text"
    )
    parser.add_argument(
        "--remove-emails", action="store_true", help="Remove email addresses from text"
    )
    parser.add_argument(
        "--remove-numbers", action="store_true", help="Remove numbers from text"
    )
    parser.add_argument(
        "--remove-emojis", action="store_true", help="Remove emojis from text"
    )
    parser.add_argument(
        "--remove-special",
        action="store_true",
        help="Remove special characters from text",
    )
    parser.add_argument(
        "--keep-chars", help="Special characters to keep (comma-separated)"
    )
    parser.add_argument(
        "--remove-diacritics", action="store_true", help="Remove diacritical marks"
    )

    args = parser.parse_args()

    # Read input text
    try:
        text = read_text_file(args.input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Process according to task
    try:
        output: Dict[str, Union[str, int, list]] = {}

        if args.task == "tokenize-words":
            word_tokenizer = BalochiWordTokenizer()
            tokens = word_tokenizer.tokenize(text)
            output = {
                "tokens": tokens,
                "token_count": len(tokens),
            }

        elif args.task == "tokenize-sentences":
            sentence_tokenizer = BalochiSentenceTokenizer()
            sentences = sentence_tokenizer.tokenize(text)
            output = {
                "sentences": sentences,
                "sentence_count": len(sentences),
            }

        elif args.task == "clean":
            cleaner = BalochiTextCleaner()
            cleaned_text = cleaner.clean_text(
                text,
                remove_numbers=args.remove_numbers,
                preserve_special_chars=not args.remove_special,
            )
            output = {
                "original_length": len(text),
                "cleaned_length": len(cleaned_text),
                "cleaned_text": cleaned_text,
            }

        elif args.task == "normalize":
            normalizer = BalochiTextNormalizer()
            normalized_text = normalizer.normalize(
                text, remove_diacritics=args.remove_diacritics
            )
            output = {
                "original_length": len(text),
                "normalized_length": len(normalized_text),
                "normalized_text": normalized_text,
            }

    except Exception as e:
        print(f"Error processing text: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Write output
    try:
        write_output(output, args.output)
    except Exception as e:
        print(f"Error writing output: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
