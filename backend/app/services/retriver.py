from typing import Dict, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import hashlib

load_dotenv()

# In-memory retriever cache keyed by transcript hash (no DB)
_retriever_cache: Dict[str, FAISS] = {}

def hash(text: str) -> str:
    """Generate a hash for the given text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def retriver(transcript: str):
    """Get or create a FAISS retriever for the given transcript."""
    transcript_hash = hash(transcript)
    
    if transcript_hash in _retriever_cache:
        return _retriever_cache[transcript_hash].as_retriever(search_type="similarity", search_kwargs={"k": 4})

    # Split transcript into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(transcript)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",   
        google_api_key=api_key,
        transport="grpc"
    )

    # Create FAISS vector store
    vector_store = FAISS.from_texts(texts, embeddings)

    # Cache the retriever
    _retriever_cache[transcript_hash] = vector_store

    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})