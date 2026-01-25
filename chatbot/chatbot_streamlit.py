import streamlit as st
from chatbot_logic import ChatbotManager

st.set_page_config(page_title="Chatbot", page_icon="🤖")

# Cache pour ne pas recharger FAISS à chaque clic
@st.cache_resource
def get_manager():
    return ChatbotManager()

try:
    manager = get_manager()
except Exception as e:
    st.error(f"Erreur démarrage: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Interaction
if question := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion..."):
            reponse = manager.generate_response(question, st.session_state.messages)
            
            st.markdown(reponse)
            st.session_state.messages.append({"role": "assistant", "content": reponse})