from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_documents import all_docs

# Clean repetitive headers from documents
for doc in all_docs:
    doc.page_content = doc.page_content.replace(
        "Laws of Cricket 2017 Code (3rd Edition - 2022)",
        ""
    )

# Create text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Split documents into chunks
chunks = splitter.split_documents(all_docs)

# Print total chunks
print(f"\nTotal chunks created: {len(chunks)}")

# Preview first chunk
print("\n================ FIRST CHUNK PREVIEW ================\n")

print(chunks[0].page_content[:1500])

print("\n====================================================")

# Print metadata of first chunk
print("\nFIRST CHUNK METADATA:\n")

print(chunks[0].metadata)