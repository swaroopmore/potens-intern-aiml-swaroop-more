from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from chunk_documents import chunks

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("\nCreating embeddings...")

# Create vector database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

print("\nVector database created successfully!")

print(f"\nTotal chunks stored: {len(chunks)}")