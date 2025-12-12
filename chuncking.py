import json
import os
import time
from configuration import settings  
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from tqdm import tqdm

load_dotenv()
api_key = os.environ.get('MISTRAL_API_KEY')

if not api_key:
    raise ValueError("Clé API manquante !")

embeddings = MistralAIEmbeddings(mistral_api_key=api_key)


with open(settings.json_clean_full_path, 'r', encoding='utf-8') as f:
    data_brute = json.load(f)

final_doc = []

print("Préparation des documents...")
for event in data_brute:
    titre = event.get('title_fr') or ""
    desc = (event.get('description_fr') or "")[:1000]
    ville = str(event.get('location_city') or "")
    
    texte_final = f"Titre: {titre}. Description: {desc}. Ville: {ville}."
    texte_final = texte_final.replace("\n", " ") 
    
    if len(texte_final) < 10:
        continue

    doc = Document(page_content=texte_final, metadata=event)
    final_doc.append(doc)

print(f"Nombre total de documents à traiter : {len(final_doc)}")

