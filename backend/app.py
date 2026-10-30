import sys
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from rag.retriever import Retriever
from rag.generator import generate_answer


app = FastAPI(
    title="Comparative Religion AI",
    description="RAG based comparative religion assistant",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


try:

    retriever = Retriever()

except Exception as e:

    retriever = None

    print(
        "Retriever could not be loaded:",
        e
    )


class QuestionRequest(BaseModel):

    question: str


@app.get("/")
def home():

    return {
        "message": "Comparative Religion AI API is running."
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:

        return {
            "answer": "Please enter a question.",
            "sources": []
        }


    if retriever is None:

        return {
            "answer": (
                "Knowledge base is not ready. "
                "Please run rag/ingest.py first."
            ),
            "sources": []
        }


    results = retriever.search(
        question,
        top_k=5
    )


    context_parts = []

    sources = []


    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['text']}"
        )

        sources.append(
            result["source"]
        )


    context = "\n\n---\n\n".join(
        context_parts
    )


    answer = generate_answer(
        question,
        context
    )


    return {
        "answer": answer,
        "sources": list(set(sources))
    }