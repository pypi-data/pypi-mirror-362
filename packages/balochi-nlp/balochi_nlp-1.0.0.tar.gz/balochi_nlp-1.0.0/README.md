# Balochi NLP

A comprehensive Natural Language Processing toolkit for the Balochi language. This package provides essential NLP tools and utilities specifically designed for processing Balochi text.

## Features

- **Text Cleaning**: Advanced text cleaning with special handling of Balochi characters
- **Tokenization**: Word and sentence tokenization with support for Balochi-specific patterns
- **Special Character Handling**: Proper handling of Balochi special characters (ءُ, ءَ, ءِ)
- **Stopwords**: Comprehensive stopword removal with customizable stopword lists
- **Morphological Analysis**: Basic support for prefix and suffix identification
- **File Processing**: Built-in support for processing large text files

## Installation

You can install the package using pip:

```bash
pip install balochi-nlp
```

For development installation:

```bash
git clone https://github.com/hafeezBaluch/balochi-nlp.git
cd balochi-nlp
pip install -e ".[dev]"
```

## Environment Setup Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setting up a Virtual Environment
It's recommended to use a virtual environment to avoid conflicts with other Python packages. Here's how to set it up:

#### Windows
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install the package
pip install balochi-nlp
```

#### macOS/Linux
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install the package
pip install balochi-nlp
```

### Deactivating the Environment
When you're done, you can deactivate the virtual environment:
```bash
deactivate
```

### Troubleshooting
- If you get a "command not found" error for Python, make sure Python is installed and added to your system's PATH.
- If you can't activate the virtual environment in Windows PowerShell, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- If you encounter permission errors, try running the commands with administrator/sudo privileges.

## Quick Start

Here's a simple example of using the package:

```python
from balochi_nlp.preprocessing import BalochiTextCleaner, BalochiStopwordRemover
from balochi_nlp.tokenizers import BalochiWordTokenizer, BalochiSentenceTokenizer

# Initialize components
cleaner = BalochiTextCleaner()
word_tokenizer = BalochiWordTokenizer()
sentence_tokenizer = BalochiSentenceTokenizer()
stopword_remover = BalochiStopwordRemover()

# Example text
text = """
منی نام احمد اِنت۔ من بلوچستان ءَ زندگ کنان۔
من روچ روچ کتابءَ وانان۔
"""

# Clean the text
cleaned_text = cleaner.clean_text(text)

# Tokenize into sentences
sentences = sentence_tokenizer.tokenize(cleaned_text)

# Process each sentence
for sentence in sentences:
    # Tokenize into words
    words = word_tokenizer.tokenize(sentence)
    # Remove stopwords
    filtered_words = stopword_remover.remove_stopwords_from_list(words)
    print(filtered_words)
```

## Documentation

For detailed documentation, visit our [documentation site](https://github.com/hafeezBaluch/balochi-nlp/tree/main/docs).

### Text Cleaning

The `BalochiTextCleaner` class provides comprehensive text cleaning capabilities:

```python
from balochi_nlp.preprocessing import BalochiTextCleaner

cleaner = BalochiTextCleaner()

# Basic cleaning
cleaned_text = cleaner.clean_text(text)

# Cleaning with options
cleaned_text = cleaner.clean_text(
    text,
    remove_numbers=True,
    preserve_special_chars=True
)
```

### Tokenization

The package provides specialized tokenizers for Balochi text:

```python
from balochi_nlp.tokenizers import BalochiWordTokenizer

tokenizer = BalochiWordTokenizer()

# Basic tokenization
tokens = tokenizer.tokenize(text)

# Tokenization with affix analysis
tokens_with_affixes = tokenizer.tokenize_with_affixes(text)
```

### Text Processing

The package provides comprehensive text processing capabilities:

```python
from balochi_nlp.preprocessing import BalochiTextCleaner, BalochiStopwordRemover

# Initialize processors
cleaner = BalochiTextCleaner()
stopword_remover = BalochiStopwordRemover()

# Clean text
cleaned_text = cleaner.clean_text(text)

# Remove stopwords
text_without_stopwords = stopword_remover.remove_stopwords(cleaned_text)

# Use custom stopwords
custom_stopwords = {"کتاب", "روچ"}  # Add domain-specific stopwords
remover = BalochiStopwordRemover(custom_stopwords=custom_stopwords)

# Or load stopwords from a file
remover = BalochiStopwordRemover(stopwords_file="path/to/custom_stopwords.txt")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{balochi_nlp2025,
  title = {Balochi NLP: A Natural Language Processing Toolkit for Balochi},
  author = {Baloch, Hafeez},
  year = {2025},
  url = {https://github.com/hafeezBaluch/balochi-nlp}
}
```

## Acknowledgments

Special thanks to all contributors and the Balochi language community for their support and feedback.

## Author

- **Hafeez Baloch** - [GitHub](https://github.com/hafeezBaluch) - [Email](mailto:hafeezullahhassan2019@gmail.com)

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/hafeezBaluch/balochi-nlp/issues) on GitHub.