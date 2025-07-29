# syntaxmatrix/file_processor.py
import os
import glob
from PyPDF2 import PdfReader
from .db import (
    add_pdf_chunk,
    delete_pdf_chunks,
    get_pdf_chunks,
    init_pdf_chunks_table
)
from .vector_db import insert_embedding, delete_embeddings_for_file
import os, openai

def extract_pdf_text(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using PyPDF2.
    """
    text = []
    with open(pdf_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)


def recursive_text_split(text: str,
                         max_length: int = 2500,
                         min_length: int = 300,
                         separators: list = [". ", "\n", " ", ""]) -> list:
    """
    Recursively splits text into chunks <= max_length using preferred separators.
    """
    text = text.strip()
    if len(text) <= max_length:
        return [text]

    split_index = -1
    for sep in separators:
        idx = text.rfind(sep, 0, max_length)
        if idx >= min_length:
            split_index = idx + len(sep)
            break

    if split_index == -1:
        split_index = max_length

    head = text[:split_index].strip()
    tail = text[split_index:].strip()
    return [head] + recursive_text_split(tail, max_length, min_length, separators)


def process_admin_pdf_files(
    directory: str,
    clear_existing: bool = True,
    max_chunk_size: int = 2500,
    min_chunk_size: int = 300
) -> dict:
    """
    Processes all PDFs in the given admin directory:
    - Extracts text
    - Splits into chunks
    - Stores chunks in the database
    - Returns an in-memory mapping of file_name -> list of chunks

    Args:
        directory (str): Path to directory containing PDFs.
        clear_existing (bool): Whether to delete existing chunks for each file before re-processing.
        max_chunk_size (int): Maximum characters per chunk.
        min_chunk_size (int): Minimum characters before splitting.

    Returns:
        dict: {file_name: [chunk1, chunk2, ...]} for all PDFs processed
    """
    # Ensure the chunks table exists
    init_pdf_chunks_table()

    result = {}
    pattern = os.path.join(directory, "*.pdf")
    pdf_paths = glob.glob(pattern)

    EMBEDDINGS_TABLE = "embeddings"
 

    from .vectorizer import embed_text 

    for pdf_path in pdf_paths:
        file_name = os.path.basename(pdf_path)
        if clear_existing:
            delete_pdf_chunks(file_name)
            delete_embeddings_for_file(file_name)

        text = extract_pdf_text(pdf_path)
        cleaned_text = " ".join(text.split())
        chunks = recursive_text_split(
            cleaned_text, max_length=max_chunk_size, min_length=min_chunk_size
        )

        for idx, chunk in enumerate(chunks):
            add_pdf_chunk(file_name, idx, chunk)

            # generate & store its embedding
            emb = embed_text(chunk)
            # Insert the embedding into the vector database
            insert_embedding(
                vector=emb,
                metadata={"file_name": file_name, "chunk_index": idx},
                chunk_text=chunk
            )
        # Store the chunks in the result dictionary
        result[file_name] = chunks
    return result

def remove_admin_pdf_file(directory: str, file_name: str):
    """
    Delete a system PDF and its stored chunks.
    """
    path = os.path.join(directory, file_name)
    if os.path.exists(path):
        os.remove(path)
    delete_pdf_chunks(file_name)
    delete_embeddings_for_file(file_name)
