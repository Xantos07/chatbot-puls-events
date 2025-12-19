import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.documents import Document
from configuration import settings

api_key = settings.mistral_api_key 

if not api_key:
    raise ValueError("Clé API Mistral manquante !")

def chunk_and_index():
    """Découpe le texte en chunks et crée l'index FAISS."""
    
    # Chemin du fichier texte
    txt_path = settings.output_dir / "evenements.txt"
    
    if not txt_path.exists():
        raise FileNotFoundError(f"❌ Fichier introuvable : {txt_path}\nExécutez d'abord export_txt.py")
    
    # Charger le texte
    print("📖 Chargement du fichier texte...")
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"📏 Taille totale du texte : {len(text)} caractères")
    
    # Créer le text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,           # Taille de chaque chunk
        chunk_overlap=200,         # Chevauchement entre chunks
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]  # Séparateurs prioritaires
    )
    
    print("✂️  Découpage du texte en chunks...")
    chunks = text_splitter.split_text(text)
    
    print(f"📦 Nombre de chunks créés : {len(chunks)}")
    return chunks
    # Convertir en Documents
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    # Créer les embeddings
    print("🧠 Création des embeddings avec Mistral...")
    embeddings = MistralAIEmbeddings(mistral_api_key=api_key)
    
    # Créer l'index FAISS
    print("💾 Création de l'index FAISS...")
    db = FAISS.from_documents(documents, embeddings)
    
    # Sauvegarder l'index
    index_path = "faiss_index_mistral"
    db.save_local(index_path)
    
    print(f"✅ Index FAISS sauvegardé dans : {index_path}")
    print(f"📊 Statistiques :")
    print(f"   - Chunks : {len(chunks)}")
    print(f"   - Chunk moyen : {sum(len(c) for c in chunks) // len(chunks)} caractères")

if __name__ == "__main__":
    chunk_and_index()
