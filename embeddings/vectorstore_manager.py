# embeddings/vectorstore_manager.py
import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.embeddings.base import Embeddings
import pickle
from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class SimpleEmbeddings(Embeddings):
    """Lightweight TF-IDF based embeddings (no ML model download needed)."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
        self.is_fitted = False
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        if not self.is_fitted:
            self.vectorizer.fit(texts)
            self.is_fitted = True
        vectors = self.vectorizer.transform(texts).toarray()
        return vectors.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        if not self.is_fitted:
            # If not fitted, fit on the query itself (fallback)
            self.vectorizer.fit([text])
            self.is_fitted = True
        vector = self.vectorizer.transform([text]).toarray()[0]
        return vector.tolist()

VSTORE_PATH = "./vector_store.faiss"
META_PATH = "./vector_store_meta.pkl"

def get_embeddings(api_key: str = None):
    """Use lightweight TF-IDF embeddings (no quota issues, no external dependencies)."""
    return SimpleEmbeddings()

def build_or_load_vectorstore(chunks: List[str], rebuild: bool = False):
    """Given text chunks, build or load a FAISS vectorstore using lightweight embeddings."""
    embeddings = get_embeddings()
    if os.path.exists(VSTORE_PATH) and not rebuild:
        try:
            vs = FAISS.load_local(VSTORE_PATH, embeddings)
            return vs
        except Exception:
            pass

    docs = [Document(page_content=c) for c in chunks]
    vs = FAISS.from_documents(docs, embeddings)
    # persist
    vs.save_local(VSTORE_PATH)
    # save metadata (if needed)
    with open(META_PATH, "wb") as f:
        pickle.dump({"n_docs": len(docs)}, f)
    return vs

def semantic_search(vectorstore, query: str, k: int = 5):
    results = vectorstore.similarity_search(query, k=k)
    return results
