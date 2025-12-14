from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="chroma_db", embedding_function=embedding)

retriever = vectordb.as_retriever()
docs = retriever.invoke("What are the side effects of metformin?")
for i, doc in enumerate(docs):
    print(f"\nDocument {i + 1}:\n{doc.page_content[:500]}")