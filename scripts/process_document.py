import json
import os

from ingestion.loader import load_documents
from ingestion.cleaner import clean_text
from ingestion.metadata import extract_metadata
from ingestion.chunker import create_chunks


# Project directories
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "handbook-master"
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


def process_documents():
    """
    Load, clean, enrich, chunk, validate,
    and save all policy documents.
    """

    print("Starting document processing...")

    # Create processed directory if it doesn't exist
    os.makedirs(
        PROCESSED_DIR,
        exist_ok=True
    )

    # 1. Load raw documents
    documents = load_documents(RAW_DIR)

    if not documents:
        print("No documents found.")
        return

    print(f"Loaded {len(documents)} documents.")

    cleaned_documents = []
    all_chunks = []

    # 2. Process every document
    for document in documents:

        file_path = document["file_path"]
        raw_text = document["text"]

        # 3. Clean text
        cleaned_text = clean_text(raw_text)

        # Skip empty documents
        if not cleaned_text:
            print(
                f"Skipping empty document: {file_path}"
            )
            continue

        # 4. Extract metadata
        metadata = extract_metadata(
            file_path,
            RAW_DIR
        )

        # 5. Save cleaned document
        cleaned_document = {
            "text": cleaned_text,
            "metadata": metadata
        }

        cleaned_documents.append(
            cleaned_document
        )

        # 6. Create chunks
        chunks = create_chunks(
            cleaned_text
        )

        # 7. Add metadata to every chunk
        for index, chunk in enumerate(chunks):

            chunk["chunk_id"] = (
                f"{metadata['source']}-{index}"
            )

            chunk["metadata"] = metadata

            all_chunks.append(chunk)

    # 8. Validate results
    if not cleaned_documents:
        print(
            "No valid documents after cleaning."
        )
        return

    if not all_chunks:
        print("No chunks were created.")
        return

    # 9. Save cleaned documents
    cleaned_output = os.path.join(
        PROCESSED_DIR,
        "cleaned_documents.json"
    )

    with open(
        cleaned_output,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cleaned_documents,
            file,
            indent=4,
            ensure_ascii=False
        )

    # 10. Save chunks
    chunks_output = os.path.join(
        PROCESSED_DIR,
        "chunks.json"
    )

    with open(
        chunks_output,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    # 11. Final summary
    print("\nDocument processing completed!")
    print(
        f"Documents processed: "
        f"{len(cleaned_documents)}"
    )
    print(
        f"Chunks created: "
        f"{len(all_chunks)}"
    )
    print(
        f"Cleaned documents: "
        f"{cleaned_output}"
    )
    print(
        f"Chunks: "
        f"{chunks_output}"
    )


if __name__ == "__main__":
    process_documents()