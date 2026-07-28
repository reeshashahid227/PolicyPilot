from sentence_transformers import SentenceTransformer

class Embedder:
    MODEL_NAME="all-MiniLM-L6-v2"

    def __init__(self,model=MODEL_NAME):
        self.model=SentenceTransformer(MODEL_NAME)
    
    def generate_embedding(self,text):
        embeddings=self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )
        return embeddings
