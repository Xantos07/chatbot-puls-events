"""
Module de découpage de texte en chunks. 
"""

import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configurations.configuration import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
def chunking(embeddings):

    """Découpe les événements JSON en chunks avec métadonnées et retourne une liste de documents.
    
    Utilise un découpage récursif rapide qui maintient la cohérence des segments.
    Plus rapide que SemanticChunker car n'utilise pas d'appels API.
    
    Returns:
        list[Document]: Liste de documents créés à partir des chunks avec métadonnées.
    
    Raises:
        FileNotFoundError: Si le fichier JSON nettoyé n'existe pas.
    """
    # Charger les événements depuis le JSON nettoyé
    json_path = settings.json_clean_full_path
    
    if not json_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        events = json.load(f)
    
    # Initialisation du splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Taille de chaque segment
        chunk_overlap=200  # Chevauchement entre les segments
    )
    
    documents = []
    total_events = len(events)
    print(f"Découpage de {total_events} événements en cours...")
    
    for idx, event in enumerate(events, 1):
        # tous les 10 événements
        if idx % 10 == 0 or idx == 1:  
            print(f"  --  Traitement événement {idx}/{total_events} ({idx*100//total_events}%)")
        # créer le texte de l'événement
        text_parts = []
        
        if event.get('title_fr'):
            text_parts.append(f"Titre: {event['title_fr']}")
        
        if event.get('description_fr'):
            text_parts.append(f"Description: {event['description_fr']}")
        
        if event.get('longdescription_fr'):
            text_parts.append(f"Détails: {event['longdescription_fr']}")
        
        if event.get('location_name'):
            text_parts.append(f"Lieu: {event['location_name']}")
        
        if event.get('location_city'):
            text_parts.append(f"Ville: {event['location_city']}")
        
        event_text = "\n".join(text_parts)
        
        # Découper le texte de l'événement en chunks
        chunks = text_splitter.split_text(event_text)
        
        # Créer des documents avec métadonnées pour chaque chunk
        for chunk in chunks:
            metadata = {
                "title": event.get('title_fr', 'N/A'),
                "date_start": event.get('timings', 'N/A'),
                "location_name": event.get('location_name', 'N/A'),
                "location_city": event.get('location_city', 'N/A'),
                "location_region": event.get('location_region', 'N/A'),
                "location_address": event.get('location_address', 'N/A'),
                "uid": event.get('uid', 'N/A')
            }
            
            documents.append(Document(page_content=chunk, metadata=metadata))
    
    print(f"Nombre de documents avec métadonnées : {len(documents)}")
    return documents
