import os
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
import streamlit as st
from mistralai import Mistral
from configuration import settings

api_key = settings.mistral_api_key

db = None
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖")

if not api_key:
    st.error("MISTRAL_API_KEY introuvable. AJoutez la dans le .env")
    st.stop()

try: 
    client = Mistral(api_key=api_key)
except Exception as e:
    st.error(f"Erreur lors de l'initialisation du client Mistral: {e}")
    st.stop()   


# déplacer dans un autre script ? 
# mettre le garde fou txt obligatoire pour éviter le brut ? 
def load_system_prompt():
    """Charge le prompt système depuis garde-fou.txt."""
    try:
        with open('garde-fou.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error("Fichier 'garde-fou.txt' introuvable. Veuillez le créer pour définir le prompt système.")
        st.session_state.messages = []
        st.stop()

# Initialiser l'historique de session Streamlit
if 'messages' not in st.session_state:
    system_prompt = load_system_prompt()
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

def main():
    st.title("🤖 Chatbot puls events")
    st.markdown("Bienvenue! Posez vos questions sur les événements à venir.")
	
    global db
    db = FAISS.load_local(settings.faiss_index_mistral, embeddings=MistralAIEmbeddings(mistral_api_key=api_key), allow_dangerous_deserialization=True)

    # historique des messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # utilisateur pose une question
    if question := st.chat_input("Posez votre question ici..."):
        # Ajouter la question de l'utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Afficher la réponse du bot
        with st.chat_message("assistant"):
            with st.spinner("Recherche des informations..."):
                # Construire le prompt avec contexte
                formatted_messages = construire_prompt_session(
                    st.session_state.messages, 
                    question, 
                    max_messages=settings.mistral_chatbot_max_messages_history
                )
                
                try:
                    response = client.chat.complete(
                    model="mistral-small-latest",  
                    messages=formatted_messages,
                    max_tokens=settings.mistral_chatbot_limit_tokens,
                    temperature=settings.mistral_chatbot_temperature,
                    top_p=settings.mistral_chatbot_top_p,
                    )
                    reponse = response.choices[0].message.content

                    print(f"reponse : {reponse}")
                    st.session_state.messages.append({"role": "assistant", "content": reponse})
                    st.markdown(reponse)
                except Exception as e:
                    st.error(f"Erreur lors de la génération de la réponse: {e}")
                    st.session_state.messages.pop()

# déplacer dans un autre script ?  
def rechercher_segments_pertinents(question, k=3):
    global db
    if db is None:
        return []

    # Récupérer les documents les plus similaires
    docs = db.similarity_search(question, k=k)
    
    # Extraire le texte pour le prompt
    segments = [doc.page_content for doc in docs]

    print("Segments pertinents récupérés :")
    for i, doc in enumerate(docs):
        print(f"{i+1}. {doc.metadata.get('title_fr', 'sans titre')} - {doc.metadata.get('location_city', '')}")
    
    return segments


def construire_prompt_session(messages, question=None, max_messages=5):
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
    
    context_segments = []
    if question:
        context_segments = rechercher_segments_pertinents(question, k=3)
    
    system_prompt = "Vous êtes l'assistant virtuel de l'entreprise puls events pour des événements "
    if context_segments:
        system_prompt += "Veuillez utiliser les informations suivantes pour répondre à la question:\n\n"
        system_prompt += "CONTEXTE:\n"
        for i, segment in enumerate(context_segments):
            system_prompt += f"[Document {i+1}]\n{segment}\n\n"
        system_prompt += "\nRÈGLES:\n- Répondez en vous basant UNIQUEMENT sur les informations fournies.\n"
    
    formatted_messages = [{"role": "system", "content": system_prompt}]
    
    for msg in recent_messages[:-1]:
        formatted_messages.append({"role": msg["role"], "content": msg["content"]})
    
    if question:
        formatted_messages.append({"role": "user", "content": question})
    
    return formatted_messages




if __name__ == "__main__":
	main()

