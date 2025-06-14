from typing import List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Load embedding + vector store
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="chroma_db", embedding_function=embedding)

def retrieve_drug_info(query: str, k: int = 2, threshold: float = 0.0) -> List[Document]:
    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": k, "score_threshold": threshold}
    )
    return retriever.get_relevant_documents(query)
