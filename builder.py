from chunking import chunking

def chat_bot_builder():
    # 1er étape : découpage du texte en chunks
    chunks = chunking()

    # 2eme étape : embedding des chunks

    # 3eme étape : création de l'index FAISS

    print(f"Création des données pour le chatbot terminée")


if __name__ == "__main__":
    chat_bot_builder()