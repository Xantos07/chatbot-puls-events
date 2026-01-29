import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
from mistralai import Mistral
from configurations.configuration import settings

class ChatbotManager:
    def __init__(self, override_db=None):
        """
        override_db: Permet d'injecter une base vectorielle temporaire pour les tests.
        """
        self.api_key = settings.mistral_api_key
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY introuvable.")

        self.client = Mistral(api_key=self.api_key)
        self.base_system_prompt = self._load_garde_fou()
        
        if override_db:
            self.db = override_db
        else:
            self.db = self._load_production_db()

    def _load_garde_fou(self):
        """Charge le garde-fou une seule fois à l'initialisation."""
        try:
            garde_fou_path = settings.garde_fou_path
            if garde_fou_path and os.path.exists(garde_fou_path):
                with open(garde_fou_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except Exception as e:
            print(f"Erreur lecture garde-fou: {e}")
        return "Vous êtes l'assistant virtuel de puls events."

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
        """Recherche les segments pertinents dans la base vectorielle."""
        if not self.db:
            return []
        
        start_time = time.perf_counter()
        docs = self.db.similarity_search(question, k=k)
        search_time = time.perf_counter() - start_time
        print(f"-----Temps recherche FAISS: {search_time:.3f}s")
        
        # Formatage du contexte
        segments = []
        for i, doc in enumerate(docs):
            txt = doc.page_content
            meta = doc.metadata
            if meta:
                txt += f"\n[Lieu: {meta.get('location_name', 'N/A')} - {meta.get('location_city', 'N/A')}]"
                txt += f"\n[Date: {meta.get('date_start', 'N/A')}]"
                txt += f"\n[Région: {meta.get('location_region', 'N/A')}]"
            segments.append(txt)
            print(f"{i+1}. {meta.get('title', 'sans titre')} - {meta.get('location_city', '')} - {meta.get('date_start', '')}")
        
        return segments

    def generate_response(self, question, history_messages, max_history=5):
        """Génère une réponse en utilisant le contexte et l'historique."""
        # Recherche du contexte
        context = self.search_context(question, k=3)
        
        # Construction du prompt système avec contexte
        system_prompt = self.base_system_prompt + "\n\n"
        if context:
            system_prompt += "Veuillez utiliser les informations suivantes pour répondre:\n\n"
            system_prompt += "CONTEXTE:\n"
            for i, segment in enumerate(context):
                system_prompt += f"[Document {i+1}]\n{segment}\n\n"
            system_prompt += "\nRÈGLES:\n- Répondez UNIQUEMENT sur la base des informations fournies.\n"
        
        # Préparer les messages pour Mistral
        formatted_messages = [{"role": "system", "content": system_prompt}]
        
        # Ajouter l'historique récent (sans les anciens system prompts)
        recent_history = history_messages[-max_history:] if len(history_messages) > max_history else history_messages
        for msg in recent_history:
            if msg["role"] != "system":  # Éviter de dupliquer le system prompt
                formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Ajouter la question actuelle
        formatted_messages.append({"role": "user", "content": question})

        # Appel API
        try:
            start_time = time.perf_counter()
            response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=formatted_messages,
                max_tokens=settings.mistral_chatbot_limit_tokens,
                temperature=settings.mistral_chatbot_temperature,
                top_p=settings.mistral_chatbot_top_p
            )
            api_time = time.perf_counter() - start_time
            print(f"-----Temps API Mistral: {api_time:.3f}s")
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Erreur lors de la génération de la réponse: {e}")