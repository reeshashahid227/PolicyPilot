from pathlib import Path

def create_chunk(text,chunk_size,overlap):
    word=text.split()
    chunks=[]
    
    chunk_id=0
    start=0

    while start<=len(word):
        end=start+chunk_size
        chunk_word=word[start:end]
        chunk_text=" ".join(chunk_word)

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text
        })

        chunk_id+=1
        start=end-overlap

    return chunks