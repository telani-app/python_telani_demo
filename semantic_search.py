import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

with open("telani_embeddings.pkl", "rb") as f:
    data = pickle.load(f)

sentences = data["sentences"]
metadata = data["metadata"]
embeddings = data["embeddings"]
model_name = data["model_name"]


model = SentenceTransformer(model_name)


def cosine_similarity(a, b):
    return np.dot(a, b)


def search(query: str, top_k: int = 5):
    query_embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores = embeddings @ query_embedding
    top_indices = scores.argsort()[::-1][:top_k]

    return [
        {
            "score": float(scores[i]),
            "sentence": sentences[i],
            "metadata": metadata[i],
        }
        for i in top_indices
    ]

print("Enter query ('exit' to terminate): ")
query = input()

while query != "exit":
    results = search(query, top_k=3)

    for r in results:
        print(f"\nScore: {r['score']:.3f}")
        print(r["sentence"])
        print(r["metadata"])

    print("Enter query:")
    query = input()

