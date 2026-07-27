import pathlib as Path
SUPPORTED_EXTENSIONS={'.md','txt'}




def load_document(data_dir):
    documents=[]

    data_dir=Path(data_dir)

    for file_path in data_dir.rglob("*"):
        if file_path.is_file()and data_dir.suffix.lower in SUPPORTED_EXTENSIONS:

            try:
                text=file_path.read_text(encoding='utf-8')

                documents.append({
                "file_name":file_path.name,
                "file_path":str(file_path),
                "text":text
                 })

            except:
                print(f"Could not load document",{file_path})
            
            return documents
                
    