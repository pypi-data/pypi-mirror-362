"""Tests for stopwords functionality."""

import os
import tempfile
from pathlib import Path

from balochi_nlp.preprocessing import BalochiStopwordRemover


def test_default_stopwords():
    """Test stopword removal with default stopwords."""
    remover = BalochiStopwordRemover()
    text = "من کتاب وانان"  # I read book
    filtered = remover.remove_stopwords(text)
    assert "من" not in filtered  # "I" should be removed
    assert "کتاب" in filtered  # "book" should remain


def test_custom_stopwords():
    """Test stopword removal with custom stopwords."""
    custom_stopwords = {"کتاب"}  # Add "book" as stopword
    remover = BalochiStopwordRemover(custom_stopwords=custom_stopwords)
    text = "من کتاب وانان"
    filtered = remover.remove_stopwords(text)
    assert "کتاب" not in filtered  # Custom stopword should be removed


def test_stopwords_from_list():
    """Test removing stopwords from a list of tokens."""
    remover = BalochiStopwordRemover()
    tokens = ["من", "کتاب", "وانان"]
    filtered = remover.remove_stopwords_from_list(tokens)
    assert "من" not in filtered
    assert "کتاب" in filtered


def test_add_stopwords():
    """Test adding new stopwords."""
    remover = BalochiStopwordRemover()
    new_stopwords = {"کتاب", "وانان"}
    remover.add_stopwords(new_stopwords)
    text = "من کتاب وانان"
    filtered = remover.remove_stopwords(text)
    assert "کتاب" not in filtered
    assert "وانان" not in filtered


def test_remove_custom_stopwords():
    """Test removing specific stopwords from the set."""
    remover = BalochiStopwordRemover()
    text = "من کتاب وانان"
    # First verify 'من' is removed
    filtered = remover.remove_stopwords(text)
    assert "من" not in filtered
    # Now remove 'من' from stopwords
    remover.remove_custom_stopwords({"من"})
    # Verify 'من' is no longer removed
    filtered = remover.remove_stopwords(text)
    assert "من" in filtered


def test_load_stopwords_from_file():
    """Test loading stopwords from a file."""
    # Create a temporary file with stopwords
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
        f.write("کتاب\nوانان\n")
        temp_path = f.name

    try:
        remover = BalochiStopwordRemover(stopwords_file=temp_path)
        text = "من کتاب وانان"
        filtered = remover.remove_stopwords(text)
        assert "کتاب" not in filtered
        assert "وانان" not in filtered
        assert "من" in filtered  # Should not be removed as it's not in the file
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_save_stopwords():
    """Test saving stopwords to a file."""
    remover = BalochiStopwordRemover()
    with tempfile.TemporaryDirectory() as temp_dir:
        save_path = Path(temp_dir) / "test_stopwords.txt"
        remover.save_stopwords(str(save_path))
        # Verify file was created and contains stopwords
        assert save_path.exists()
        with open(save_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "من" in content  # Default stopword should be in file


def test_empty_text():
    """Test handling of empty text."""
    remover = BalochiStopwordRemover()
    assert remover.remove_stopwords("") == ""
    assert remover.remove_stopwords_from_list([]) == []


def test_no_stopwords_in_text():
    """Test text with no stopwords."""
    remover = BalochiStopwordRemover()
    text = "کتاب قلم"  # No stopwords in this text
    assert remover.remove_stopwords(text) == text
