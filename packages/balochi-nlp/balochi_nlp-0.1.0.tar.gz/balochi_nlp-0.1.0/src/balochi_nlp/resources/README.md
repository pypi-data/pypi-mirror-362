# Resources Directory

This directory contains various resources used by the Balochi NLP package.

## Directory Structure

- `stopwords/`: Contains stopword lists for Balochi language
  - `balochi.txt`: Default Balochi stopwords
- `data/`: Contains sample texts and corpora for testing and examples

## Adding New Resources

When adding new resources:
1. Place them in the appropriate subdirectory
2. Update this README.md file
3. Update MANIFEST.in in the root directory
4. Add appropriate tests if needed

## File Formats

### Stopwords Files
- One word per line
- UTF-8 encoding
- Comments start with '#'
- Blank lines are ignored

### Data Files
- Text files should be in UTF-8 encoding
- Include source attribution where applicable
- Document any special formatting requirements 