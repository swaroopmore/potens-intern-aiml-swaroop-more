import os
from dotenv import load_dotenv

from groq import Groq

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector database
db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# User query
query = input("\nAsk your cricket question: ")

# Retrieve relevant chunks
results = db.similarity_search(query, k=3)

# Build context
context = "\n\n".join([doc.page_content for doc in results])

# Prompt
prompt = f"""
You are a cricket document assistant.

Answer ONLY from the provided context.

If the context contains partial information,
answer using ONLY that information.

If the answer is completely missing,
reply:
"The documents do not contain enough information."

Context:
{context}

Question:
{query}
"""

# Generate response using Groq
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

# Print AI answer
print("\n================ AI ANSWER ================\n")

print(response.choices[0].message.content)

print("\n===========================================")

# Print citations
print("\n================ CITATIONS ================\n")

for i, doc in enumerate(results):

    print(f"Citation {i+1}")

    print(f"Source File: {doc.metadata.get('source_file')}")

    print(f"Page Number: {doc.metadata.get('page')}")

    print("\nSnippet:\n")

    print(doc.page_content[:300])

    print("\n-------------------------------------------")