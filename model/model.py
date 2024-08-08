from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks

def process_and_store_data(data):
    embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    documents = []
    for item in data:
        if isinstance(item, dict) and "text" in item:
            chunks = chunk_text(item["text"])
            for chunk in chunks:
                documents.append(Document(page_content=chunk, metadata=item))
        elif isinstance(item, str):
            chunks = chunk_text(item)
            for chunk in chunks:
                documents.append(Document(page_content=chunk))

    if documents:
        vector_store = FAISS.from_documents(documents, embeddings)
        print(f"Created vector store with {len(documents)} documents.")
        return vector_store
    else:
        print("No valid documents to process. Creating an empty vector store.")
        return FAISS.from_texts(["No data available"], embeddings)

