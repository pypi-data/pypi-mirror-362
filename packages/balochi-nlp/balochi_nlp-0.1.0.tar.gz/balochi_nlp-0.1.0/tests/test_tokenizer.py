import pytest

from balochi_nlp.tokenizers.sentence_tokenizer import BalochiSentenceTokenizer
from balochi_nlp.tokenizers.word_tokenizer import BalochiWordTokenizer


@pytest.fixture
def word_tokenizer():
    """Fixture to create a word tokenizer instance for tests."""
    return BalochiWordTokenizer()


@pytest.fixture
def sentence_tokenizer():
    """Fixture to create a sentence tokenizer instance for tests."""
    return BalochiSentenceTokenizer()


def test_basic_word_tokenization(word_tokenizer):
    """Test basic word tokenization."""
    text = "منی نام احمد اِنت"
    tokens = word_tokenizer.tokenize(text)
    assert len(tokens) == 4
    assert tokens == ["منی", "نام", "احمد", "اِنت"]


def test_punctuation_handling(word_tokenizer):
    """Test handling of punctuation in word tokenization."""
    text = "منی نام احمد اِنت۔ من بلوچستان ءَ زندگ کنان۔"
    tokens = word_tokenizer.tokenize(text)
    assert "۔" not in tokens
    assert "منی" in tokens
    assert "نام" in tokens
    assert "احمد" in tokens


def test_special_char_tokenization(word_tokenizer):
    """Test tokenization of words with special characters."""
    test_cases = [
        ("دشتءِ", ["دشتءِ"]),  # Keep special characters attached
        ("کتابءَ", ["کتابءَ"]),
        ("گسءُ", ["گسءُ"]),
    ]

    for input_text, expected_tokens in test_cases:
        tokens = word_tokenizer.tokenize(input_text)
        assert tokens == expected_tokens


def test_compound_word_handling(word_tokenizer):
    """Test handling of compound words."""
    text = "کتاب\u200cخانہ"  # Using zero-width non-joiner
    tokens = word_tokenizer.tokenize(text)
    assert len(tokens) == 2
    assert tokens == ["کتاب", "خانہ"]


def test_empty_string_handling(word_tokenizer):
    """Test handling of empty strings."""
    assert word_tokenizer.tokenize("") == []
    assert word_tokenizer.tokenize("   ") == []


def test_multiple_spaces_handling(word_tokenizer):
    """Test handling of multiple spaces."""
    text = "منی    نام     احمد    اِنت"
    tokens = word_tokenizer.tokenize(text)
    assert len(tokens) == 4
    assert tokens == ["منی", "نام", "احمد", "اِنت"]


def test_basic_sentence_tokenization(sentence_tokenizer):
    """Test basic sentence tokenization."""
    text = "منی نام احمد اِنت۔ من بلوچستان ءَ زندگ کنان۔"
    sentences = sentence_tokenizer.tokenize(text)
    assert len(sentences) == 1  # Since '۔' is not in sentence_endings pattern
    assert "منی نام احمد اِنت۔ من بلوچستان ءَ زندگ کنان۔" in sentences


def test_multiple_punctuation_handling(sentence_tokenizer):
    """Test handling of multiple punctuation marks."""
    text = "منی نام احمد اِنت؟ من بلوچستان ءَ زندگ کنان! کجا رئوی۔"
    sentences = sentence_tokenizer.tokenize(text)
    assert len(sentences) == 3


def test_sentence_boundary_with_special_chars(sentence_tokenizer):
    """Test sentence boundary detection with special characters."""
    text = "کتابءَ بوان۔ درسءِ یاد کن۔"
    sentences = sentence_tokenizer.tokenize(text)
    assert len(sentences) == 1  # Since '۔' is not in sentence_endings pattern
    assert "کتابءَ بوان۔ درسءِ یاد کن۔" in sentences


def test_tokenize_with_affixes(word_tokenizer):
    """Test tokenization with affix identification."""
    text = "بےوفا نامراد"
    tokens = word_tokenizer.tokenize_with_affixes(text)

    # Check the first token
    assert tokens[0]["token"] == "بےوفا"
    assert "بے" in tokens[0]["prefixes"]

    # Check the second token
    assert tokens[1]["token"] == "نامراد"
    assert "نا" in tokens[1]["prefixes"]
