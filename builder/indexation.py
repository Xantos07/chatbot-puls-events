import json
import time
from langchain_community.vectorstores import FAISS
import psutil
from prometheus_client import Histogram, Gauge
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configurations.configuration import settings

# Définir les métriques
INDEXATION_TIME = Histogram('indexation_duration_seconds', 'Durée de l\'indexation')
INDEXATION_MEMORY = Gauge('indexation_memory_mb', 'Mémoire utilisée pendant l\'indexation (MB)')

def indexation(documents, embeddings):
    """Crée et sauvegarde l'index FAISS à partir des documents et embeddings."""
    print("\n" + "="*60)
    print("DÉBUT DE L'INDEXATION")
    print("="*60)
    
    # Mesurer le temps manuellement
    start_time = time.time()
    
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024
    
    print(f"Mémoire avant indexation : {mem_before:.2f} MB")
    print(f"Nombre de documents : {len(documents)}")
    print("Création de l'index FAISS...")
    
    db = FAISS.from_documents(documents, embeddings)

    index_path = settings.output_dir / settings.faiss_index_mistral
    db.save_local(str(index_path))
    
    mem_after = process.memory_info().rss / 1024 / 1024
    mem_used = mem_after - mem_before
    
    # Calculer la durée
    duration = time.time() - start_time
    
    print(f"Mémoire après indexation : {mem_after:.2f} MB")
    print(f"Mémoire utilisée : {mem_used:.2f} MB")
    print(f"Durée d'indexation : {duration:.2f} secondes")
    print(f"Index FAISS sauvegardé dans : {index_path}")
    
    # Enregistrer les métriques Prometheus
    INDEXATION_MEMORY.set(mem_used)
    INDEXATION_TIME.observe(duration)
    
    print(f" Métrique INDEXATION_MEMORY définie à : {mem_used:.2f} MB")
    print(f" Métrique INDEXATION_TIME définie à : {duration:.2f} s")
    
    # Sauvegarder dans un fichier JSON
    metrics = {
        'indexation_memory_mb': mem_used,
        'indexation_duration_seconds': duration,
        'timestamp': time.time()
    }
    
    # mettre dans configuration ! 
    metrics_file = settings.output_dir / 'metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f)
    
    print(f" Métriques sauvegardées dans : {metrics_file}")

    print("="*60)
    print("FIN DE L'INDEXATION")
    print("="*60 + "\n")
    
    return db