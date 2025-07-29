# Balochi Stopwords

This directory contains stopword lists for the Balochi language.

## Files

- `balochi.txt`: Default Balochi stopwords list
  - Contains common pronouns, prepositions, conjunctions, and other function words
  - Organized by word categories (pronouns, prepositions, etc.)
  - Each word is accompanied by an English translation in comments

## File Format

The stopwords files follow this format:
```
# Category name
word1    # English translation
word2    # English translation

# Another category
word3    # English translation
```

## Contributing

To add or modify stopwords:
1. Ensure the word is actually a stopword (common function word with little semantic value)
2. Add it under the appropriate category
3. Include an English translation as a comment
4. Keep the file organized and well-documented
5. Submit a pull request with your changes

## Usage

The stopwords can be used through the `BalochiStopwordRemover` class:

```python
from balochi_nlp.preprocessing import BalochiStopwordRemover

# Use default stopwords
remover = BalochiStopwordRemover()

# Or use a custom stopwords file
remover = BalochiStopwordRemover(stopwords_file="path/to/custom_stopwords.txt")
``` 