'''
Script d'exportation des événements OpenAgenda vers un fichier texte formaté.
mais inutile pour le chunking actuel.
'''

import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configurations.configuration import settings

def export_to_txt():
    """Exporte les événements du fichier JSON nettoyé vers un fichier texte formaté"""

    with open(settings.json_clean_full_path, 'r', encoding='utf-8') as f:
        events = json.load(f)
    
    output_path = settings.output_dir / settings.txt_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, event in enumerate(events):
            # Titre
            f.write(f"=== ÉVÉNEMENT {i+1} ===\n")
            f.write(f"Titre: {event.get('title_fr', 'N/A')}\n\n")
            
            # Description
            if event.get('description_fr'):
                f.write(f"Description: {event.get('description_fr')}\n\n")
            
            # Longue description
            if event.get('longdescription_fr'):
                f.write(f"Détails: {event.get('longdescription_fr')}\n\n")
            
            # Horaires
            if event.get('timings'):
                f.write(f"Horaires: {event.get('timings')}\n\n")
            
            # Lieu
            f.write(f"Lieu: {event.get('location_name', 'N/A')}\n")
            f.write(f"Adresse: {event.get('location_address', 'N/A')}\n")
            f.write(f"Ville: {event.get('location_city', 'N/A')} ({event.get('location_postalcode', 'N/A')})\n")
            f.write(f"Région: {event.get('location_region', 'N/A')}\n\n")
            
            # Conditions
            if event.get('conditions_fr'):
                f.write(f"Conditions: {event.get('conditions_fr')}\n\n")
            
            # Inscription
            if event.get('registration'):
                f.write(f"Inscription: {event.get('registration')}\n\n")
            
            # Contact
            if event.get('location_phone'):
                f.write(f"Téléphone: {event.get('location_phone')}\n")
            if event.get('location_website'):
                f.write(f"Site web: {event.get('location_website')}\n")
            
            # Age
            if event.get('age_min') or event.get('age_max'):
                f.write(f"\nÂge: {event.get('age_min', 'N/A')} - {event.get('age_max', 'N/A')} ans\n")
            
            # Séparation
            f.write("\n" + "="*80 + "\n\n")
    
    print(f"Fichier exporté : {output_path}")
    print(f"Nombre d'événements exportés : {len(events)}")

if __name__ == "__main__":
    export_to_txt()
