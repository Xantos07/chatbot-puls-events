"""
Module de découpage de texte en chunks. 
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from configuration import settings  
from langchain_core.documents import Document

# Exporter les chunks
def chunking():

    # Chemin du fichier texte
    txt_path = settings.output_dir / "evenements.txt"

    if not txt_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {txt_path}")
    
    # Charger le texte
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
        
    chunks = text_splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    print(f"Nombre de chunks : {len(chunks)}")
    return documents
