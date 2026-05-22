from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_documents import all_docs

# Create text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# Split documents into chunks
chunks = splitter.split_documents(all_docs)

# Print total chunks
print(f"\nTotal chunks created: {len(chunks)}")

# Preview first chunk
print("\n================ FIRST CHUNK PREVIEW ================\n")

print(chunks[0].page_content)

print("\n====================================================")

# Print metadata of first chunk
print("\nFIRST CHUNK METADATA:\n")

print(chunks[0].metadata)