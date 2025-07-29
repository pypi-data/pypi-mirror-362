import pytest

from balochi_nlp.preprocessing.cleaner import BalochiTextCleaner


@pytest.fixture
def cleaner():
    """Fixture to create a cleaner instance for tests."""
    return BalochiTextCleaner()


def test_basic_cleaning(cleaner):
    """Test basic text cleaning functionality."""
    text = "منی نام احمد اِنت۔ https://example.com user@email.com 123 ABC"
    cleaned = cleaner.clean_text(text)
    assert "https://example.com" not in cleaned
    assert "user@email.com" not in cleaned
    assert "123" not in cleaned
    assert "ABC" not in cleaned
    assert "منی نام احمد" in cleaned


def test_special_char_handling(cleaner):
    """Test handling of special Balochi characters."""
    test_cases = [
        ("دشتءِ", ["دشت", "ءِ"]),  # Should split into two tokens
        ("کتابءَ", ["کتاب", "ءَ"]),  # Should split into two tokens
        ("گسءُ", ["گس", "ءُ"]),  # Should split into two tokens
    ]

    for input_text, expected_parts in test_cases:
        cleaned = cleaner.clean_text(input_text)
        for part in expected_parts:
            assert part in cleaned


def test_whitespace_normalization(cleaner):
    """Test whitespace normalization."""
    text = "منی    نام     احمد    اِنت۔"
    cleaned = cleaner.clean_text(text)
    assert "    " not in cleaned
    assert cleaned.count(" ") == cleaned.count(" ")  # No duplicate spaces


def test_punctuation_handling(cleaner):
    """Test handling of Balochi punctuation marks."""
    text = "منی نام احمد اِنت۔ من بلوچستان ءَ زندگ کنان۔"
    cleaned = cleaner.clean_text(text)
    assert "۔" not in cleaned  # Punctuation should be removed
    assert "منی نام احمد" in cleaned
    assert "من بلوچستان" in cleaned


def test_number_removal_option(cleaner):
    """Test the number removal option."""
    text = "منی نام احمد 123 اِنت۔"
    # With number removal (default)
    cleaned_with_removal = cleaner.clean_text(text, remove_numbers=True)
    assert "123" not in cleaned_with_removal

    # Without number removal
    cleaned_without_removal = cleaner.clean_text(text, remove_numbers=False)
    assert "123" in cleaned_without_removal


def test_special_chars_preservation_option(cleaner):
    """Test the special characters preservation option."""
    text = "دشتءِ کتابءَ گسءُ"

    # With special chars preservation (default)
    cleaned_with_preservation = cleaner.clean_text(text, preserve_special_chars=True)
    assert "ءِ" in cleaned_with_preservation
    assert "ءَ" in cleaned_with_preservation
    assert "ءُ" in cleaned_with_preservation

    # Without special chars preservation
    cleaned_without_preservation = cleaner.clean_text(
        text, preserve_special_chars=False
    )
    assert "ءِ" not in cleaned_without_preservation
    assert "ءَ" not in cleaned_without_preservation
    assert "ءُ" not in cleaned_without_preservation


def test_url_and_email_removal(cleaner):
    """Test removal of URLs and email addresses."""
    text = """
    منی ویب سایٹ https://example.com اِنت۔
    منی ای میل user@email.com اِنت۔
    """
    cleaned = cleaner.clean_text(text)
    assert "https://example.com" not in cleaned
    assert "user@email.com" not in cleaned
    assert "منی ویب سایٹ" in cleaned
    assert "منی ای میل" in cleaned


def test_emoji_removal(cleaner):
    """Test removal of emojis."""
    text = "منی نام احمد 😊 اِنت۔ من خوش 🌟 آن۔"
    cleaned = cleaner.clean_text(text)
    assert "😊" not in cleaned
    assert "🌟" not in cleaned
    assert "منی نام احمد" in cleaned
    assert "من خوش آن" in cleaned


def test_file_cleaning(cleaner, tmp_path):
    """Test cleaning text from a file."""
    # Create a temporary test file
    test_file = tmp_path / "test.txt"
    test_content = "منی نام احمد اِنت۔ https://example.com user@email.com"
    test_file.write_text(test_content, encoding="utf-8")

    # Clean the file
    cleaned = cleaner.clean_file(str(test_file))
    assert "https://example.com" not in cleaned
    assert "user@email.com" not in cleaned
    assert "منی نام احمد" in cleaned
