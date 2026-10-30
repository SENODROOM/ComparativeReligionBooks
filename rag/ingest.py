import os
import json
import numpy as np
import faiss

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LIBRARY_DIR = os.path.join(BASE_DIR, "library")
DATA_DIR = os.path.join(BASE_DIR, "data")

CHUNKS_FILE = os.path.join(DATA_DIR, "chunks.json")
INDEX_FILE = os.path.join(DATA_DIR, "index.faiss")


MODEL_NAME = "all-MiniLM-L6-v2"


def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return text


def split_text(text, chunk_size=1000, overlap=150):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def main():

    os.makedirs(DATA_DIR, exist_ok=True)

    all_chunks = []

    print("Scanning library...")

    for root, dirs, files in os.walk(LIBRARY_DIR):

        for file in files:

            if file.lower().endswith(".pdf"):

                pdf_path = os.path.join(root, file)

                print(f"Processing: {file}")

                text = extract_text_from_pdf(pdf_path)

                chunks = split_text(text)

                for chunk in chunks:

                    all_chunks.append({
                        "text": chunk,
                        "source": file
                    })

    if not all_chunks:
        print("No PDF text found.")
        return

    print(f"Total chunks: {len(all_chunks)}")

    print("Creating embeddings...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [item["text"] for item in all_chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)

    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            all_chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Knowledge base created successfully!")
    print(f"Saved: {CHUNKS_FILE}")
    print(f"Saved: {INDEX_FILE}")


if __name__ == "__main__":
    main()