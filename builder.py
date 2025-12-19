from chunking import chunking
from embeddings import embed_documents

def chat_bot_builder():
    # 1er étape : découpage du texte en chunks retournant les documents
    documents = chunking()

    # 2eme étape : embedding des chunks
    embeddings = embed_documents(documents)

    # 3eme étape : création de l'index FAISS
    
    print(f"Création des données pour le chatbot terminée")


if __name__ == "__main__":
    chat_bot_builder()