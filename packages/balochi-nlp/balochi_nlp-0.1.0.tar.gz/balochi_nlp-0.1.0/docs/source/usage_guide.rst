Usage Guide
===========

This guide provides examples and explanations for using the Balochi NLP package.

Text Cleaning
------------

The package provides comprehensive text cleaning capabilities through the ``BalochiTextCleaner`` class:

.. code-block:: python

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

Stopword Removal
--------------

Remove common Balochi stopwords from text using the ``BalochiStopwordRemover`` class:

.. code-block:: python

    from balochi_nlp.preprocessing import BalochiStopwordRemover

    # Initialize with default stopwords
    remover = BalochiStopwordRemover()

    # Remove stopwords from text
    text_without_stopwords = remover.remove_stopwords(text)

    # Remove stopwords from a list of tokens
    filtered_tokens = remover.remove_stopwords_from_list(tokens)

    # Use custom stopwords
    custom_stopwords = {"کتاب", "روچ"}  # Add domain-specific stopwords
    remover = BalochiStopwordRemover(custom_stopwords=custom_stopwords)

    # Load stopwords from a file
    remover = BalochiStopwordRemover(stopwords_file="path/to/custom_stopwords.txt")

    # Add more stopwords to existing set
    remover.add_stopwords({"new", "stopwords"})

    # Save current stopwords to file
    remover.save_stopwords("path/to/save/stopwords.txt")

Tokenization
-----------

The package provides specialized tokenizers for Balochi text:

Word Tokenization
~~~~~~~~~~~~~~~

.. code-block:: python

    from balochi_nlp.tokenizers import BalochiWordTokenizer

    tokenizer = BalochiWordTokenizer()
    
    # Basic tokenization
    tokens = tokenizer.tokenize(text)

Sentence Tokenization
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from balochi_nlp.tokenizers import BalochiSentenceTokenizer

    tokenizer = BalochiSentenceTokenizer()
    
    # Split text into sentences
    sentences = tokenizer.tokenize(text)

Complete Example
--------------

Here's a complete example showing how to use multiple components together:

.. code-block:: python

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

    # Process sentences
    sentences = sentence_tokenizer.tokenize(cleaned_text)
    
    # Process each sentence
    for sentence in sentences:
        # Tokenize into words
        words = word_tokenizer.tokenize(sentence)
        # Remove stopwords
        filtered_words = stopword_remover.remove_stopwords_from_list(words)
        print(filtered_words)

Advanced Features
---------------

For more advanced features and detailed examples, please refer to the API Reference section. 