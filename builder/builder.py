from builder.chunking import chunking
from builder.embeddings import get_mistral_embeddings
from builder.indexation import indexation

def chat_bot_builder():
    """Construit les données pour le chatbot :
    - Découpage du texte en chunks
    - Création des embeddings
    - Création de l'index FAISS
    """
    # 2eme étape : embedding des chunks
    embeddings = get_mistral_embeddings()

    # 1er étape : découpage du texte en chunks retournant les documents
    documents = chunking(embeddings)

    # 3eme étape : création de l'index FAISS
    indexation(documents, embeddings)

    print(f"Création des données pour le chatbot terminée")


if __name__ == "__main__":
    chat_bot_builder()