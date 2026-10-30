import os
import json
import faiss

from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

CHUNKS_FILE = os.path.join(DATA_DIR, "chunks.json")
INDEX_FILE = os.path.join(DATA_DIR, "index.faiss")

MODEL_NAME = "all-MiniLM-L6-v2"


class Retriever:

    def __init__(self):

        if not os.path.exists(CHUNKS_FILE):
            raise FileNotFoundError(
                "chunks.json not found. Run ingest.py first."
            )

        if not os.path.exists(INDEX_FILE):
            raise FileNotFoundError(
                "index.faiss not found. Run ingest.py first."
            )

        self.model = SentenceTransformer(MODEL_NAME)

        self.index = faiss.read_index(INDEX_FILE)

        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)


    def search(self, question, top_k=5):

        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True
        )

        query_embedding = query_embedding.astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(distances[0], indices[0]):

            if index < len(self.chunks):

                result = self.chunks[index].copy()

                result["distance"] = float(distance)

                results.append(result)

        return results