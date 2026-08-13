from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def get_embeddings(texts:list[str])-> list[list[float]]:
    return model.encode(texts).tolist()
