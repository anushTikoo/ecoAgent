from google import genai
from google.genai import types
import os

async def embed_text(text):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    result = client.models.embed_content(
        model = "gemini-embedding-001",
        contents = text,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    )
    return result.embeddings