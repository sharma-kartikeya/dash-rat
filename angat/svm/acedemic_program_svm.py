import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_API_KEY")

sentence = "Machine learning is transforming various industries."

# Generate the embedding using the text-embedding-ada-002 model
response = openai.Embedding.create(
  input=sentence,
  model="text-embedding-ada-002"
)

# Extract the embedding vector
embedding = response['data'][0]['embedding']

print("Embedding vector:", embedding)
print("Embedding length:", len(embedding))