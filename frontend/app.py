import streamlit as st
import requests

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Cricket RAG System",
    page_icon="🏏",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🏏 Cricket RAG System")

st.markdown("""
Ask questions about cricket documents and compare rules across documents.
""")

# ==========================================
# TABS
# ==========================================

tab1, tab2 = st.tabs(["Ask Questions", "Contradict Analysis"])

# ==========================================
# ASK TAB
# ==========================================

with tab1:

    st.header("Ask Cricket Questions")

    question = st.text_input(
        "Enter your question:"
    )

    if st.button("Get Answer"):

        if question.strip() != "":

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                    "question": question
                }
            )

            data = response.json()

            st.subheader("Answer")

            st.write(data["answer"])

            st.subheader("Citations")

            for citation in data["citations"]:

                st.markdown(f"""
                **Source File:** {citation['source_file']}

                **Page Number:** {citation['page_number']}

                **Snippet:**
                {citation['snippet']}
                """)

                st.divider()

# ==========================================
# CONTRADICT TAB
# ==========================================

with tab2:

    st.header("Document Contradiction Analysis")

    doc1 = st.text_input(
        "Document 1 Filename"
    )

    doc2 = st.text_input(
        "Document 2 Filename"
    )

    topic = st.text_input(
        "Topic to Compare"
    )

    if st.button("Analyze Contradiction"):

        if doc1 and doc2 and topic:

            response = requests.post(
                "http://127.0.0.1:8000/contradict",
                json={
                    "doc1": doc1,
                    "doc2": doc2,
                    "topic": topic
                }
            )

            data = response.json()

            st.subheader("Analysis")

            st.write(data["analysis"])