import pandas as pd
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings

def inject_medlineplus_to_chroma(csv_path="data/medlineplus_drugs.csv", persist_dir="chroma_db"):
    df = pd.read_csv(csv_path, sep=";")

    docs = []
    for _, row in df.iterrows():
        text = (
            f"Drug: {row['drug_name']}\n"
            f"Uses: {row['uses']}\n"
            f"Side Effects: {row['side_effects']}\n"
            f"Precautions: {row['precautions']}\n"
            f"Source: {row['url']}"
        )
        docs.append(Document(page_content=text, metadata={"source": row["url"]}))

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    vectordb.persist()
    print("Documents embedded:", vectordb._collection.count())  

if __name__ == "__main__":
    inject_medlineplus_to_chroma()