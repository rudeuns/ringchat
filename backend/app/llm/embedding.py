from langchain_community.embeddings import OpenAIEmbeddings
from typing import List


def generate_embedding(text: str, model_type: str = "openai") -> List[float]:
    if model_type == "openai":
        return generate_openai_embedding(text)
    else:
        raise ValueError("Unsupported model_type.")


def generate_openai_embedding(text: str) -> List[float]:
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-ada-002"
    )  # 1536 dim
    embedding_vector = embedding_model.embed_query(text)
    return embedding_vector
