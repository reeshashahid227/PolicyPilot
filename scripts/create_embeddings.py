import json
import os
import sys

import numpy as np
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)

from src.embeddings.embedder import Embedder
from src.embeddings.vector_store import VectorStore


# --------------------------------------------------
# Project directories
# --------------------------------------------------


PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

CHUNKS_FILE = os.path.join(
    PROCESSED_DIR,
    "chunks.json"
)

EMBEDDINGS_FILE = os.path.join(
    PROCESSED_DIR,
    "embeddings.npy"
)

INDEX_FILE = os.path.join(
    PROCESSED_DIR,
    "policy.index"
)

METADATA_FILE = os.path.join(
    PROCESSED_DIR,
    "vector_metadata.json"
)


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():


    # --------------------------------------------------
    # 1. Check input file
    # --------------------------------------------------

    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}"
        )

    # --------------------------------------------------
    # 2. Load chunks
    # --------------------------------------------------

    print("\n[1/5] Loading chunks...")

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError(
            "No chunks found in chunks.json"
        )

    print(f"Total chunks: {len(chunks)}")

    # --------------------------------------------------
    # 3. Extract text
    # --------------------------------------------------

    print("\n[2/5] Extracting chunk text...")

    texts = []

    for chunk in chunks:

        text = chunk.get("text", "").strip()

        if text:
            texts.append(text)

    if not texts:
        raise ValueError(
            "No valid chunk text found."
        )

    print(
        f"Valid texts: {len(texts)}"
    )

    # --------------------------------------------------
    # 4. Generate embeddings
    # --------------------------------------------------

    print("\n[3/5] Loading embedding model...")

    embedder = Embedder()

    print(
        "Generating embeddings..."
    )

    embeddings = embedder.generate_embeddings(
        texts
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    # --------------------------------------------------
    # 5. Save embeddings
    # --------------------------------------------------

    print("\n[4/5] Saving embeddings...")

    np.save(
        EMBEDDINGS_FILE,
        embeddings
    )

    print(
        f"Saved: {EMBEDDINGS_FILE}"
    )

    # --------------------------------------------------
    # 6. Build FAISS index
    # --------------------------------------------------

    print("\n[5/5] Building FAISS index...")

    dimension = embeddings.shape[1]

    vector_store = VectorStore(
        dimension=dimension
    )

    vector_store.add_embeddings(
        embeddings
    )

    vector_store.save(
        INDEX_FILE
    )

    print(
        f"FAISS index saved: {INDEX_FILE}"
    )

    # --------------------------------------------------
    # 7. Save metadata mapping
    # --------------------------------------------------

    metadata = []

    for index, chunk in enumerate(chunks):

        metadata.append(
            {
                "vector_id": index,
                "chunk_id": chunk.get(
                    "chunk_id",
                    index
                ),
                "metadata": chunk.get(
                    "metadata",
                    {}
                )
            }
        )

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Metadata saved: {METADATA_FILE}"
    )

    # --------------------------------------------------
    # Final summary
    # --------------------------------------------------

  

    print(
        f"Chunks:       {len(chunks)}"
    )

    print(
        f"Embeddings:   {embeddings.shape}"
    )

    print(
        f"FAISS index:  {INDEX_FILE}"
    )

    print(
        f"Metadata:     {METADATA_FILE}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()