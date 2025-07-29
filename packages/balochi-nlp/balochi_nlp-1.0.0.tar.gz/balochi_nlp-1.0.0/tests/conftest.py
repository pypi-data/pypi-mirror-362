import tempfile

import pytest


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture(scope="session")
def sample_balochi_text():
    """Return a sample Balochi text for testing."""
    return """
    منی نام احمد اِنت۔ من بلوچستان ءَ زندگ کنان۔
    من روچ روچ کتابءَ وانان۔ منی لوٹ اِش اِنت کہ من وتی زبانءَ گیش زانان۔
    من وتی درسءِ یات کنان۔ من مزنیں آدمے بیاں۔
    """


@pytest.fixture(scope="session")
def sample_mixed_text():
    """Return a sample text with mixed content for testing cleaning."""
    return """
    Hello World! منی نام احمد اِنت۔
    Email: user@example.com
    Website: https://example.com
    Phone: 123-456-7890
    Emoji: 😊 🌟
    """


@pytest.fixture(scope="session")
def sample_special_chars():
    """Return a sample text with special Balochi characters."""
    return "دشتءِ کتابءَ گسءُ"


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "cleaner: mark test as cleaner related")
    config.addinivalue_line("markers", "tokenizer: mark test as tokenizer related")
    config.addinivalue_line("markers", "integration: mark test as integration test")
