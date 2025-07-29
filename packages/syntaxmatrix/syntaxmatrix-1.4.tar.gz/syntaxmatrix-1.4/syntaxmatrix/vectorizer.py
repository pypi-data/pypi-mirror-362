import os
import openai
from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=EMBEDDING_KEY)

def embed_text(text: str):
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        encoding_format="float"
    )

    return resp.data[0].embedding
    
def get_embeddings_in_batches(texts, batch_size=100):
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small", # Or your chosen model
                input=batch
            )
            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)
        except openai.APITimeoutError:
            print(f"Timeout occurred on batch starting at index {i}. Skipping.")
            # You could also add retry logic here
        except Exception as e:
            print(f"An error occurred on batch {i}: {e}")
    return all_embeddings