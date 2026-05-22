# 🏏 Cricket RAG System

An AI-powered Retrieval-Augmented Generation (RAG) system for cricket documents using FastAPI, ChromaDB, Groq LLMs, semantic search, and multilingual support.

Built as part of the Potens AI/ML Internship Assignment.

---

# Features

## ✅ Document Question Answering
- Ask questions about cricket laws, IPL rules, DLS methodology, and playing conditions.
- Answers are grounded strictly in retrieved document context.

## ✅ Citation Support
Every answer includes:
- source file
- page number
- retrieved snippet

## ✅ Contradiction Analysis
Compare two documents on a topic and determine:
- contradictions
- consistency
- reasoning

## ✅ Multilingual Support
Queries can be asked in:
- English
- Hindi
- Marathi
- Spanish
- other languages

The system responds in the same language as the user query.

## ✅ Hallucination Prevention
If documents do not contain enough information, the system explicitly says so instead of generating fake answers.

## ✅ Streamlit Frontend
Simple UI for:
- asking questions
- contradiction analysis

---

# Tech Stack

## Backend
- FastAPI

## Vector Database
- ChromaDB

## Embedding Model
- sentence-transformers/all-MiniLM-L6-v2

## LLM
- Groq API
- Llama 3.3 70B Versatile

## Frontend
- Streamlit

## Document Processing
- LangChain
- PyPDF

---

# Project Architecture

```text
PDF Documents
      ↓
Document Loader
      ↓
Chunking
      ↓
Embeddings
      ↓
Chroma Vector Database
      ↓
Semantic Retrieval
      ↓
Groq LLM
      ↓
Grounded Answer Generation
      ↓
Citations / Contradiction Analysis
```

---

# Documents Used

- IPL Playing Conditions
- MCC Laws of Cricket
- DLS Methodology PDF
- ICC T20 Playing Conditions
- Cricket Analytics Research Paper

---

# Chunking Strategy

Used RecursiveCharacterTextSplitter with:

- chunk_size = 1000
- chunk_overlap = 200

### Why?

Cricket law and playing-condition documents contain long contextual rules. Larger chunks preserve semantic continuity and improve retrieval quality.

### Additional Optimization

Repetitive document headers were removed before chunking because they negatively affected embedding quality and semantic retrieval accuracy.

---

# Hallucination Prevention Strategy

The prompt explicitly instructs the LLM to:

- answer ONLY from retrieved context
- avoid generating unsupported claims
- state when information is missing

This ensures grounded responses instead of silent hallucinations.

---

# API Endpoints

## `/ask`

### POST Request

```json
{
  "question": "What is the DLS method?"
}
```

### Response

```json
{
  "question": "...",
  "answer": "...",
  "citations": [...]
}
```

---

## `/contradict`

### POST Request

```json
{
  "doc1": "IPL.pdf",
  "doc2": "MCC.pdf",
  "topic": "powerplay rules"
}
```

### Response

```json
{
  "analysis": "..."
}
```

---

# How To Run

## 1. Clone Repository

```bash
git clone <your_repo_link>
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate.bat
```

---

## 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 5. Add Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 6. Create Vector Database

```bash
python backend/create_vectorstore.py
```

---

## 7. Start FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

---

## 8. Start Streamlit Frontend

```bash
streamlit run frontend/app.py
```

---

# Swagger API Docs

Available at:

```text
http://127.0.0.1:8000/docs
```

---

# Design Decisions

## Why ChromaDB?

Chosen because:
- lightweight
- local persistence
- fast setup for 24-hour assignment scope

## Why Groq?

Groq provides:
- fast inference
- free API access
- reliable Llama models

## Why Sentence Transformers?

`all-MiniLM-L6-v2` provides:
- lightweight embeddings
- strong semantic search quality
- fast local inference

---

# Challenges Faced

## 1. Retrieval Noise
Initial retrieval quality suffered because repeated PDF headers polluted embeddings.

### Solution
Removed repetitive headers before chunking.

---

## 2. Gemini API Limitations
Gemini free-tier quotas caused rate-limit failures.

### Solution
Migrated answer generation pipeline to Groq.

---

# Future Improvements

- Hybrid search (BM25 + vector search)
- Reranking layer
- Confidence scoring
- Human-in-the-loop approval
- Conversation memory
- Better document filtering
- Production deployment

---

# Known Limitations

- Retrieval quality depends on document structure.
- Contradiction analysis may miss subtle semantic conflicts.
- No authentication layer.
- Current multilingual support is prompt-based rather than translation-based.

---

# AI Usage Log

## ChatGPT
Approx. 250+ messages

Used for:
- architecture planning
- debugging
- retrieval optimization
- FastAPI integration
- prompt engineering
- vector database setup
- multilingual support
- README preparation

## GitHub Copilot
Used occasionally for boilerplate completion and syntax suggestions.

---

# Author

Swaroop More

MCA Student — MIT-WPU Pune