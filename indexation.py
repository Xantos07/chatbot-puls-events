
from langchain_community.vectorstores import FAISS
from configuration import settings

def indexation(documents, embeddings):
    """Crée et sauvegarde l'index FAISS à partir des documents et embeddings.
    
    Args:
        documents: Liste de documents à indexer.
        embeddings: Objet embeddings MistralAI.
    """
    print("FAISS")
    db = FAISS.from_documents(documents, embeddings)

    index_path = settings.output_dir / settings.faiss_index_mistral
    db.save_local(index_path)
    