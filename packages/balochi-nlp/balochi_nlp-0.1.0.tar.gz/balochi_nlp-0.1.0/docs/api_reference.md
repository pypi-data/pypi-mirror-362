# API Reference

This document provides detailed information about the Balochi NLP package's modules, classes, and functions.

## Text Preprocessing

### BalochiTextCleaner

```python
from balochi_nlp.preprocessing import BalochiTextCleaner

cleaner = BalochiTextCleaner()
```

Class for cleaning and normalizing Balochi text.

#### Methods

##### clean_text
```python
def clean_text(
    text: str,
    remove_numbers: bool = True,
    preserve_special_chars: bool = True
) -> str:
    """Clean and normalize Balochi text.

    Args:
        text: Input text to clean
        remove_numbers: Whether to remove numerical digits
        preserve_special_chars: Whether to preserve Balochi special characters

    Returns:
        Cleaned text string
    """
```

##### clean_file
```python
def clean_file(
    file_path: str,
    encoding: str = 'utf-8'
) -> str:
    """Clean text from a file.

    Args:
        file_path: Path to the input file
        encoding: File encoding (default: utf-8)

    Returns:
        Cleaned text string
    """
```

### BalochiNormalizer

```python
from balochi_nlp.preprocessing import BalochiNormalizer

normalizer = BalochiNormalizer()
```

#### Methods

##### normalize_text
```python
def normalize_text(text: str) -> str:
    """Normalize Balochi text by standardizing characters and diacritics.

    Args:
        text: Input text to normalize

    Returns:
        Normalized text string
    """
```

## Tokenization

### BalochiWordTokenizer

```python
from balochi_nlp.tokenizers import BalochiWordTokenizer

tokenizer = BalochiWordTokenizer()
```

Class for tokenizing Balochi text into words.

#### Methods

##### tokenize
```python
def tokenize(text: str) -> List[str]:
    """Tokenize Balochi text into words.

    Args:
        text: Input text to tokenize

    Returns:
        List of word tokens
    """
```

##### tokenize_with_affixes
```python
def tokenize_with_affixes(text: str) -> List[Dict[str, str]]:
    """Tokenize text and identify prefixes and suffixes.

    Args:
        text: Input text to tokenize

    Returns:
        List of dictionaries containing:
        - token: The main word token
        - prefix: Identified prefix (if any)
        - suffix: Identified suffix (if any)
    """
```

### BalochiSentenceTokenizer

```python
from balochi_nlp.tokenizers import BalochiSentenceTokenizer

sentence_tokenizer = BalochiSentenceTokenizer()
```

Class for tokenizing Balochi text into sentences.

#### Methods

##### tokenize
```python
def tokenize(text: str) -> List[str]:
    """Split Balochi text into sentences.

    Args:
        text: Input text to split into sentences

    Returns:
        List of sentence strings
    """
```

## Utility Functions

### File Processing

```python
from balochi_nlp.utils.file_utils import read_text_file, write_text_file

def read_text_file(
    file_path: str,
    encoding: str = 'utf-8'
) -> str:
    """Read text from a file.

    Args:
        file_path: Path to the input file
        encoding: File encoding (default: utf-8)

    Returns:
        Text content of the file
    """

def write_text_file(
    text: str,
    file_path: str,
    encoding: str = 'utf-8'
) -> None:
    """Write text to a file.

    Args:
        text: Text to write
        file_path: Path to the output file
        encoding: File encoding (default: utf-8)
    """
```

## Examples

### Basic Text Processing

```python
from balochi_nlp.preprocessing import BalochiTextCleaner
from balochi_nlp.tokenizers import BalochiWordTokenizer, BalochiSentenceTokenizer

# Initialize components
cleaner = BalochiTextCleaner()
word_tokenizer = BalochiWordTokenizer()
sentence_tokenizer = BalochiSentenceTokenizer()

# Example text
text = """
منی نام احمد اِنت۔ من بلوچستان ءَ زندگ کنان۔
من روچ روچ کتابءَ وانان۔
"""

# Clean the text
cleaned_text = cleaner.clean_text(text)

# Tokenize into sentences
sentences = sentence_tokenizer.tokenize(cleaned_text)

# Tokenize each sentence into words
for sentence in sentences:
    words = word_tokenizer.tokenize(sentence)
    print(words)
```

### File Processing

```python
from balochi_nlp.preprocessing import BalochiTextCleaner
from balochi_nlp.utils.file_utils import read_text_file, write_text_file

# Initialize cleaner
cleaner = BalochiTextCleaner()

# Read input file
text = read_text_file('input.txt')

# Clean the text
cleaned_text = cleaner.clean_text(text)

# Write cleaned text to file
write_text_file(cleaned_text, 'output.txt')
```

## Support

For questions and issues:
1. Check the [documentation](https://github.com/hafeezBaluch/balochi-nlp/tree/main/docs)
2. Search existing [issues](https://github.com/hafeezBaluch/balochi-nlp/issues)
3. Create a new issue if needed
4. Contact the maintainer: Hafeez Baloch (hafeezullahhassan2019@gmail.com) 