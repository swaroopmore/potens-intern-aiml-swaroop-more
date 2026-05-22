import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel

from groq import Groq

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

# ==========================================
# INITIALIZE FASTAPI
# ==========================================

app = FastAPI(
    title="Cricket RAG System",
    description="AI-powered cricket document question answering system with citations and contradiction analysis.",
    version="1.0"
)

# ==========================================
# INITIALIZE GROQ CLIENT
# ==========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# LOAD VECTOR DATABASE
# ==========================================

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# ==========================================
# REQUEST MODELS
# ==========================================

class QuestionRequest(BaseModel):
    question: str


class ContradictRequest(BaseModel):
    doc1: str
    doc2: str
    topic: str

# ==========================================
# /ask ENDPOINT
# ==========================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    query = request.question

    # Retrieve relevant chunks
    results = db.similarity_search(query, k=5)

    # Build context
    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    # Prompt
    prompt = f"""
    You are a multilingual cricket document assistant.

    IMPORTANT RULES:
    - Answer ONLY from the provided context.
    - Answer in the SAME language as the user's question.
    - If the context contains partial information,
      answer using ONLY that information.
    - If the answer is completely missing,
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

    # Final response
    return {
        "question": query,
        "answer": response.choices[0].message.content,
        "citations": citations
    }

# ==========================================
# /contradict ENDPOINT
# ==========================================

@app.post("/contradict")
def contradict_documents(request: ContradictRequest):

    # Retrieve chunks from document 1
    results_doc1 = db.similarity_search(
        request.topic,
        k=3,
        filter={"source_file": request.doc1}
    )

    # Retrieve chunks from document 2
    results_doc2 = db.similarity_search(
        request.topic,
        k=3,
        filter={"source_file": request.doc2}
    )

    # Build contexts
    context_doc1 = "\n\n".join(
        [doc.page_content for doc in results_doc1]
    )

    context_doc2 = "\n\n".join(
        [doc.page_content for doc in results_doc2]
    )

    # Prompt
    prompt = f"""
    You are a cricket document comparison assistant.

    Compare the following two document contexts.

    Determine whether they conflict on the topic:
    "{request.topic}"

    IMPORTANT RULES:
    - ONLY use the provided contexts.
    - Clearly explain contradictions if present.
    - If there is no contradiction,
      explain why they are consistent.
    - Keep the explanation concise but clear.

    ==============================
    DOCUMENT 1 CONTEXT
    ==============================

    {context_doc1}

    ==============================
    DOCUMENT 2 CONTEXT
    ==============================

    {context_doc2}
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

    # Final response
    return {
        "topic": request.topic,
        "doc1": request.doc1,
        "doc2": request.doc2,
        "analysis": response.choices[0].message.content
    }