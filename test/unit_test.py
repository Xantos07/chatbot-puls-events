import pytest
import json
import sys
import os
from unittest.mock import MagicMock, patch

# ajout du dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from builder.chunking import chunking 
from builder.indexation import indexation 
from builder.embeddings import get_mistral_embeddings
from configurations.configuration import settings
from langchain_core.documents import Document

@pytest.fixture
def real_embeddings():
    """
    Fixture pour obtenir les embeddings MistralAI
    """
    return get_mistral_embeddings()

# ---JSON TEMPORAIRE ---
@pytest.fixture
def test_json_file(tmp_path):
    event_data = [{
        "title_fr": "Comptines et chansons à la bibliothèque",
        "description_fr": "Comptines et chansons avec Jérôme et sa guitare",
        "longdescription_fr": "Comptines et chansons avec Jérôme et sa guitare, de l'association Filofil, qui enchante les petites oreilles des 0-3 ans. Un moment privilégié à la médiathèque de Moulins, où les plaisirs de la lecture partagée et de l'écoute musicale sont au rendez-vous.",
        "conditions_fr": "Réservation indispensable",
        "timings": "Le 29/03/2025 de 10:15 à 11:30",
        "location_name": "médiathèque de Moulins",
        "location_address": "8 allée de la Filature 59 000 Lille",
        "location_insee": 59350,
        "location_postalcode": 59000,
        "location_city": "Lille",
        "location_department": "Nord",
        "location_region": "Hauts-de-France",
        "location_countrycode": "FR",
        "age_min": None,
        "age_max": 3,
        "registration": "phone: 03 28 55 30 93",
        "location_phone": "03 28 55 30 93",
        "location_website": "http://bm-lille.fr",
        "uid": "UID_LILLE"
    }, {
        "title_fr": "Auditions « Grange Dimière » - « Absolution » 🎼",
        "description_fr": "Extraits du « Dernier jour d’un condamné » de Victor HUGO et du discours de Robert BADINTER à l’Assemblée Nationale. Avec les Classes à Horaires Aménagés Théâtre du Collège Robert BADINTER",
        "longdescription_fr": "📆 Mardi 10 Décembre 🕖 17H30 & 19H00 Professeur : Fanny BAYARD, Caroline PANZERA, Gwenaëlle TANCHON",
        "conditions_fr": "Aucune condition précisée",
        "timings": "Le 10/12/2024 de 17:30 à 19:00 / Le 10/12/2024 de 19:00 à 20:30",
        "location_name": "La Grange Dimière Cambrai",
        "location_address": "4 Rue Saint-Julien, 59400 Cambrai",
        "location_insee": 59122,
        "location_postalcode": 59400,
        "location_city": "Cambrai",
        "location_department": "Nord",
        "location_region": "Hauts-de-France",
        "location_countrycode": "FR",
        "age_min": None,
        "age_max": None,
        "registration": "Voir description",
        "location_phone": "pas de numéro de téléphone",
        "location_website": "pas de site",
        "uid": "UID_Cambrai"
    }
    
    ]
    
    p = tmp_path / "test_events.json"
    # On convertit le dict Python en string JSON
    p.write_text(json.dumps(event_data), encoding='utf-8')
    return p


# ==========================================
# TEST FONCTION CHUNKING
# ==========================================

def test_chunking(real_embeddings, test_json_file):
    """
    Teste que la fonction découpe bien le texte et attache les métadonnées.
    """
    
    with patch('builder.chunking.settings') as mock_settings:
        mock_settings.json_clean_full_path = test_json_file
        
        documents = chunking(real_embeddings)
        
        print(f"\n Total chunks générés : {len(documents)}")
        
        # On cherche les documents de LILLE
        # On filtre la liste pour ne garder que ceux qui ont l'UID de Lille
        docs_lille = [d for d in documents if d.metadata["uid"] == "UID_LILLE"]
        
        print(f" Chunks pour Lille : {len(docs_lille)}")
        assert len(docs_lille) > 0, "Aucun chunk trouvé pour Lille !"
        assert docs_lille[0].metadata["location_city"] == "Lille"
        assert "Comptines" in " ".join([d.page_content for d in docs_lille])
        
        # On cherche les documents de CAMBRAI
        docs_cambrai = [d for d in documents if d.metadata["uid"] == "UID_Cambrai"]
        
        print(f" Chunks pour Cambrai : {len(docs_cambrai)}")
        assert len(docs_cambrai) > 0, "Aucun chunk trouvé pour Cambrai !"
        assert docs_cambrai[0].metadata["location_city"] == "Cambrai"
        
        texte_cambrai = " ".join([d.page_content for d in docs_cambrai])
        assert "Assemblée Nationale" in texte_cambrai
        assert "Comptines" not in texte_cambrai
        
        print("\n Test réussi : Lille et Cambrai sont bien séparés")

# ==========================================
# TEST INDEXATION 
# ==========================================

def test_indexation(real_embeddings):
    # Données tests
    docs = [Document(page_content="Test contenu", metadata={"id": 1})]
    
    # patch de FAISS
    with patch('builder.indexation.FAISS') as MockFAISS:
        
        indexation(docs, real_embeddings)
        
        # Vérifications
        MockFAISS.from_documents.assert_called_once()
        
        # On vérifie qu'on a essayé de sauvegarder
        mock_db_instance = MockFAISS.from_documents.return_value
        mock_db_instance.save_local.assert_called_once()
        
        print("\n Test Indexation réussi (FAISS mocké).")