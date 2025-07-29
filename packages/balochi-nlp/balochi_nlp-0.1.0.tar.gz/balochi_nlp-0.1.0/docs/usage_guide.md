# Usage Guide

This guide provides detailed examples and best practices for using the Balochi NLP package.

## Basic Usage

### Text Cleaning

```python
from balochi_nlp.preprocessing import BalochiTextCleaner

# Initialize the cleaner
cleaner = BalochiTextCleaner()

# Example text
text = """
منی نام احمد اِنت۔ https://example.com
من بلوچستان ءَ زندگ کنان۔ user@email.com
من روچ روچ کتابءَ وانان۔ 123 ABC
"""

# Basic cleaning
cleaned_text = cleaner.clean_text(text)
print(cleaned_text)

# Cleaning with options
cleaned_text = cleaner.clean_text(
    text,
    remove_numbers=True,
    preserve_special_chars=True
)
print(cleaned_text)
```

### Tokenization

#### Word Tokenization

```python
from balochi_nlp.tokenizers import BalochiWordTokenizer

# Initialize tokenizer
tokenizer = BalochiWordTokenizer()

# Example text
text = "منی نام احمد اِنت۔"

# Basic tokenization
tokens = tokenizer.tokenize(text)
print(tokens)

# Tokenization with affix analysis
tokens_with_affixes = tokenizer.tokenize_with_affixes(text)
for token_info in tokens_with_affixes:
    print(f"Token: {token_info['token']}")
    if token_info.get('prefix'):
        print(f"Prefix: {token_info['prefix']}")
    if token_info.get('suffix'):
        print(f"Suffix: {token_info['suffix']}")
```

#### Sentence Tokenization

```python
from balochi_nlp.tokenizers import BalochiSentenceTokenizer

# Initialize tokenizer
sentence_tokenizer = BalochiSentenceTokenizer()

# Example text
text = """
منی نام احمد اِنت۔
من بلوچستان ءَ زندگ کنان۔
من روچ روچ کتابءَ وانان۔
"""

# Split into sentences
sentences = sentence_tokenizer.tokenize(text)
for sentence in sentences:
    print(sentence)
```

## Advanced Usage

### Processing Files

```python
from balochi_nlp.preprocessing import BalochiTextCleaner
from balochi_nlp.utils.file_utils import read_text_file, write_text_file

# Initialize components
cleaner = BalochiTextCleaner()

# Read and process a file
input_text = read_text_file('input.txt')
cleaned_text = cleaner.clean_text(input_text)
write_text_file(cleaned_text, 'output.txt')

# Process multiple files
import glob
import os

input_dir = 'input_files'
output_dir = 'output_files'
os.makedirs(output_dir, exist_ok=True)

for input_file in glob.glob(os.path.join(input_dir, '*.txt')):
    # Read input file
    text = read_text_file(input_file)
    
    # Clean text
    cleaned_text = cleaner.clean_text(text)
    
    # Create output filename
    output_file = os.path.join(
        output_dir,
        os.path.basename(input_file)
    )
    
    # Write cleaned text
    write_text_file(cleaned_text, output_file)
```

### Combined Processing Pipeline

```python
from balochi_nlp.preprocessing import BalochiTextCleaner
from balochi_nlp.tokenizers import BalochiWordTokenizer, BalochiSentenceTokenizer

def process_text(text):
    """Complete text processing pipeline."""
    # Initialize components
    cleaner = BalochiTextCleaner()
    word_tokenizer = BalochiWordTokenizer()
    sentence_tokenizer = BalochiSentenceTokenizer()
    
    # Clean the text
    cleaned_text = cleaner.clean_text(text)
    
    # Split into sentences
    sentences = sentence_tokenizer.tokenize(cleaned_text)
    
    # Process each sentence
    results = []
    for sentence in sentences:
        # Tokenize words
        words = word_tokenizer.tokenize(sentence)
        
        # Analyze words (example)
        word_count = len(words)
        
        # Store results
        results.append({
            'sentence': sentence,
            'words': words,
            'word_count': word_count
        })
    
    return results

# Example usage
text = """
منی نام احمد اِنت۔
من بلوچستان ءَ زندگ کنان۔
من روچ روچ کتابءَ وانان۔
"""

results = process_text(text)
for result in results:
    print(f"Sentence: {result['sentence']}")
    print(f"Words: {result['words']}")
    print(f"Word count: {result['word_count']}\n")
```

## Best Practices

1. **Always Clean Text First**
   - Remove unwanted characters
   - Normalize special characters
   - Handle URLs and emails appropriately

2. **Use Virtual Environments**
   - Create a new environment for each project
   - Keep dependencies isolated
   - Avoid version conflicts

3. **Error Handling**
   ```python
   try:
       cleaned_text = cleaner.clean_text(text)
   except Exception as e:
       print(f"Error cleaning text: {e}")
       # Handle error appropriately
   ```

4. **Memory Efficiency**
   - Process large files in chunks
   - Use generators for large datasets
   - Clean up resources properly

5. **Performance Optimization**
   - Reuse initialized objects
   - Process in batches when possible
   - Use appropriate data structures

## Common Issues and Solutions

### 1. Character Encoding
```python
# Always specify encoding when reading files
text = read_text_file('input.txt', encoding='utf-8')
```

### 2. Memory Management
```python
# Process large files in chunks
def process_large_file(file_path, chunk_size=1024):
    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk
```

### 3. Error Handling
```python
def safe_process(text):
    try:
        return cleaner.clean_text(text)
    except UnicodeError:
        # Handle encoding errors
        return text
    except Exception as e:
        # Log error and handle appropriately
        print(f"Error: {e}")
        return None
```

## Getting Help

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/hafeezBaluch/balochi-nlp/tree/main/docs)
2. Search existing [issues](https://github.com/hafeezBaluch/balochi-nlp/issues)
3. Create a new issue if needed
4. Contact the maintainer: Hafeez Baloch (hafeezullahhassan2019@gmail.com) 