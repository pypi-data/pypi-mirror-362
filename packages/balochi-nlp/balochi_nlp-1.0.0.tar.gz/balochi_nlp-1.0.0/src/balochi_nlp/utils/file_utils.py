"""Utility functions for processing large text files."""

import os
from typing import Callable, Iterator, Optional

from tqdm import tqdm


def process_large_file(
    file_path: str,
    chunk_size: int = 1024 * 1024,  # 1MB chunks
    processor: Optional[Callable[[str], str]] = None,
    encoding: str = "utf-8",
    show_progress: bool = True,
) -> Iterator[str]:
    """
    Process a large text file in chunks to avoid memory issues.

    Args:
        file_path: Path to the text file
        chunk_size: Size of chunks to read (in bytes)
        processor: Optional function to process each chunk
        encoding: File encoding (default: utf-8)
        show_progress: Whether to show progress bar

    Yields:
        Processed text chunks
    """
    file_size = os.path.getsize(file_path)

    with open(file_path, "r", encoding=encoding) as file:
        with tqdm(total=file_size, disable=not show_progress) as pbar:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                if processor:
                    chunk = processor(chunk)

                pbar.update(len(chunk.encode(encoding)))
                yield chunk


def save_processed_text(
    input_path: str,
    output_path: str,
    processor: Callable[[str], str],
    chunk_size: int = 1024 * 1024,
    encoding: str = "utf-8",
    show_progress: bool = True,
) -> None:
    """
    Process a large text file and save the results.

    Args:
        input_path: Path to input file
        output_path: Path to save processed text
        processor: Function to process the text
        chunk_size: Size of chunks to read
        encoding: File encoding
        show_progress: Whether to show progress bar
    """
    with open(output_path, "w", encoding=encoding) as out_file:
        for chunk in process_large_file(
            input_path,
            chunk_size=chunk_size,
            processor=processor,
            encoding=encoding,
            show_progress=show_progress,
        ):
            out_file.write(chunk)
