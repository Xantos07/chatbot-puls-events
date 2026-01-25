import os
import time
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
from mistralai import Mistral
from configurations.configuration import settings

class ChatbotManager:
    # override_db pour les tests unitaires
    def __init__(self, override_db=None):
        """
        override_db: Permet d'injecter une base vectorielle temporaire pour les tests.
        """
        self.api_key = settings.mistral_api_key
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY introuvable.")

        self.client = Mistral(api_key=self.api_key)
        
        if override_db:
            self.db = override_db
        else:
            self.db = self._load_production_db()

    def _load_production_db(self):
        try:
            return FAISS.load_local(
                settings.output_dir / settings.faiss_index_mistral, 
                embeddings=MistralAIEmbeddings(mistral_api_key=self.api_key), 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Erreur chargement DB: {e}")
            return None

    def search_context(self, question, k=3):
        if not self.db:
            return []
        
        # Recherche FAISS
        docs = self.db.similarity_search(question, k=k)
        
        # Formatage du contexte
        segments = []
        for doc in docs:
            txt = doc.page_content
            meta = doc.metadata
            if meta:
                txt += f"\n[Date: {meta.get('date_start', 'N/A')}]"
                txt += f"\n[Lieu: {meta.get('location_city', 'N/A')}]"
            segments.append(txt)
        return segments

    def generate_response(self, question, history_messages):
        # contexte
        context = self.search_context(question)
        
        # prompt système
        system_prompt = "Vous êtes l'assistant puls events. "
        if context:
            system_prompt += "Utilisez ce contexte :\n" + "\n\n".join(context)
        
        # Préparer les messages pour Mistral
        # On convertit le format Streamlit en format Mistral si besoin
        formatted_messages = [{"role": "system", "content": system_prompt}]
        
        # On ajoute l'historique récent (sans le system prompt précédent)
        for msg in history_messages[-5:]: 
            if msg["role"] != "system":
                formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        
        formatted_messages.append({"role": "user", "content": question})

        # appel API
        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=formatted_messages,
            temperature=0.7
        )
        return response.choices[0].message.content