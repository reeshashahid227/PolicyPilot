from pathlib import Path

def extract_metadata(file_path,root_dir):

    file_path=Path(file_path)
    root_dir=Path(root_dir)

    relative_path=file_path.relative_to(root_dir)
    parts=relative_path.parts

    if len(parts)>0:
        catagory=parts[0]
    else:
        catagory="general"
    
    return{
        "source":file_path.name,
        "catagory":catagory,
        "file_type":file_path.suffix.lower().replace(".",""),
        "relative_path":str(relative_path)
    }