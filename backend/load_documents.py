from langchain_community.document_loaders import PyPDFLoader
import os

# Folder containing PDFs
DOCS_PATH = "documents"

# Store all loaded pages
all_docs = []

# Read all files inside documents folder
for file in os.listdir(DOCS_PATH):

    # Process only PDF files
    if file.endswith(".pdf"):

        # Create full file path
        path = os.path.join(DOCS_PATH, file)

        print(f"\nLoading {file}...")

        # Load PDF
        loader = PyPDFLoader(path)

        # Extract pages
        docs = loader.load()

        # Add source filename into metadata
        for doc in docs:
            doc.metadata["source_file"] = file

        # Add all pages to master list
        all_docs.extend(docs)

# Total pages loaded
print(f"\nTotal pages loaded: {len(all_docs)}")

# Preview first page
print("\n================ FIRST PAGE PREVIEW ================\n")

print(all_docs[0].page_content[:1000])

print("\n====================================================")