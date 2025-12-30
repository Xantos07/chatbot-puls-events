"""
Module de découpage de texte en chunks. 
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configurations.configuration import settings

def chunking():
    """Découpe le fichier texte en chunks et retourne une liste de documents.
    
    Returns:
        list[Document]: Liste de documents créés à partir des chunks.
    
    Raises:
        FileNotFoundError: Si le fichier evenements.txt n'existe pas.
    """

    # Chemin du fichier texte
    txt_path = settings.output_dir / "evenements.txt"
    print(f"txt_path: {txt_path}")
    
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
