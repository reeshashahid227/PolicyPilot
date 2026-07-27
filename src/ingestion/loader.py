from pathlib import Path


SUPPORTED_EXTENSIONS = {".md", ".txt"}


def load_documents(data_dir):
    """
    Load all supported documents from the given directory.
    """

    documents = []

    data_dir = Path(data_dir)

    for file_path in data_dir.rglob("*"):

        if (
            file_path.is_file()
            and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
        ):

            try:
                text = file_path.read_text(
                    encoding="utf-8"
                )

                documents.append({
                    "file_name": file_path.name,
                    "file_path": str(file_path),
                    "text": text
                })

            except UnicodeDecodeError:
                print(f"Could not decode: {file_path}")

    return documents