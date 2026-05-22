import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel

from groq import Groq

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ==============================
# LOAD ENV VARIABLES
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

# ==============================
# INITIALIZE FASTAPI
# ==============================

app = FastAPI()

# ==============================
# INITIALIZE GROQ
# ==============================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==============================
# LOAD EMBEDDING MODEL
# ==============================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==============================
# LOAD VECTOR DATABASE
# ==============================

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# ==============================
# REQUEST MODEL
# ==============================

class QuestionRequest(BaseModel):
    question: str

# ==============================
# /ask ENDPOINT
# ==============================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    query = request.question

    # Retrieve relevant chunks
    results = db.similarity_search(query, k=5)

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

    # Generate response
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

    # Build citations
    citations = []

    for doc in results:

        citations.append({
            "source_file": doc.metadata.get("source_file"),
            "page_number": doc.metadata.get("page"),
            "snippet": doc.page_content[:300]
        })

    # Final API response
    return {
        "question": query,
        "answer": response.choices[0].message.content,
        "citations": citations
    }