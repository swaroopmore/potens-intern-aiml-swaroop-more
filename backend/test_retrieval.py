from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load existing vector database
db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# User query
query = "What are the powerplay rules in cricket?"

print("\nSearching relevant chunks...\n")

# Retrieve top 3 relevant chunks
results = db.similarity_search(query, k=3)

# Print results
for i, result in enumerate(results):

    print(f"\n================ RESULT {i+1} ================\n")

    print(result.page_content[:1000])

    print("\n--------------- METADATA ---------------\n")

    print(result.metadata)

    print("\n========================================")