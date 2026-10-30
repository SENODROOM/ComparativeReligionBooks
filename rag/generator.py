import os
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()


# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")


# Create Gemini client
client = genai.Client(api_key=API_KEY)


def generate_answer(question, context):
    """
    Generate an answer using Gemini based on retrieved book content.
    """

    prompt = f"""
You are AnonymousThinker, a knowledge-based AI assistant.

Answer the user's question using the provided source material.

Rules:
- Use the provided source material as your primary source.
- Do not invent quotes, books, authors, or references.
- If the source material does not contain enough information, clearly say so.
- Clearly distinguish information from the books from your own explanation.
- Be respectful when discussing religious beliefs and different viewpoints.
- Do not present religious interpretations as scientific facts.
- Give a clear and helpful answer.
- Keep the answer reasonably concise.

SOURCE MATERIAL:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text