
from langchain_community.vectorstores import FAISS

def indexation(documents, embeddings):
    print("FAISS")
    db = FAISS.from_documents(documents, embeddings)

    index_path = "faiss_index_mistral"
    db.save_local(index_path)
    