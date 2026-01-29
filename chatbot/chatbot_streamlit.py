import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from chatbot_logic import ChatbotManager

# Cache pour ne pas recharger FAISS à chaque clic
@st.cache_resource
def get_manager():
    return ChatbotManager()

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Chatbot puls events")
st.markdown("Bienvenue! Posez vos questions sur les événements à venir.")

try:
    manager = get_manager()
except Exception as e:
    st.error(f"Erreur au démarrage: {e}")
    st.stop()

# Initialiser l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Interaction utilisateur
if question := st.chat_input("Posez votre question ici..."):
    # Ajouter la question à l'historique
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").markdown(question)

    # Générer la réponse
    with st.chat_message("assistant"):
        with st.spinner("Recherche des informations..."):
            try:
                reponse = manager.generate_response(
                    question, 
                    st.session_state.messages,
                    max_history=5
                )
                st.markdown(reponse)
                st.session_state.messages.append({"role": "assistant", "content": reponse})
            except Exception as e:
                st.error(f"Erreur: {e}")
                # Retirer la question de l'historique en cas d'erreur
                st.session_state.messages.pop()