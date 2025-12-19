from langchain_mistralai import MistralAIEmbeddings
from mistralai import Mistral
import os
from pathlib import Path
from configuration import settings
import numpy as np


api_key = settings.mistral_api_key

if not api_key:
    raise EnvironmentError("MISTRAL_API_KEY introuvable.")

client = Mistral(api_key=api_key)

def get_mistral_embeddings():
    """Crée et retourne les embeddings MistralAI.
    
    Returns:
        MistralAIEmbeddings: L'objet embeddings pour l'indexation.
    """
    print("embeddings")
    embeddings = MistralAIEmbeddings(mistral_api_key=api_key)
    return embeddings

def embed(text: str):
    """Encode le texte en vecteur d'embedding en utilisant MistralAI.
    
    Args:
        text (str): Le texte à encoder.
    
    Returns:
        np.ndarray: Le vecteur d'embedding.
    """
    try:
        response = client.embeddings.create(
            model="mistral-embed",
            inputs=[text]
        )
        return np.array(response.data[0].embedding)
    except Exception as e:
        return f"Erreur : {e}"
