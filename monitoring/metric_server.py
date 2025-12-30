from prometheus_client import start_http_server, Gauge
import time
import json
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configurations.configuration import settings

INDEXATION_MEMORY = Gauge('indexation_memory_mb', 'Mémoire utilisée pendant l\'indexation (MB)')
INDEXATION_DURATION = Gauge('indexation_duration_seconds', 'Durée de l\'indexation')

def load_metrics():
    """Charge les métriques depuis le fichier JSON."""
    metrics_file = settings.output_dir / 'metrics.json'
    
    if metrics_file.exists():
        try:
            with open(metrics_file, 'r') as f:
                metrics = json.load(f)
            
            mem = metrics.get('indexation_memory_mb', 0)
            dur = metrics.get('indexation_duration_seconds', 0)
            
            INDEXATION_MEMORY.set(mem)
            INDEXATION_DURATION.set(dur)
            
            return mem, dur, True
        except Exception as e:
            print(f" Erreur de lecture : {e}")
            return 0, 0, False
    else:
        return 0, 0, False

def run_metrics_server(port=8001):
    """Lance un serveur Prometheus dédié qui reste actif en permanence."""
    print("="*60)
    print("SERVEUR DE MÉTRIQUES PROMETHEUS")
    print("="*60)
    
    metrics_file = settings.output_dir / 'metrics.json'
    print(f"\n Fichier de métriques : {metrics_file}")
    print(f"   Existe ? {metrics_file.exists()}")
    
    # Charger les métriques existantes au démarrage
    print("\n Chargement des métriques...")
    mem, dur, success = load_metrics()
    
    if success:
        print(f" Métriques chargées avec succès :")
        print(f"  - Mémoire : {mem:.2f} MB")
        print(f"  - Durée : {dur:.2f} s")
    else:
        print(" Aucune métrique trouvée. En attente de builder.py...")
    
    # le serveur
    print(f"\n Démarrage du serveur HTTP...")
    start_http_server(port)
    print(f" Serveur actif sur le port {port}")
    print(f" URL : http://localhost:{port}/metrics")
    print("\n" + "="*60)
    print("Surveillance active - Appuyez sur Ctrl+C pour arrêter")
    print("="*60 + "\n")
    
    last_mtime = 0
    
    try:
        while True:
            if metrics_file.exists():
                current_mtime = metrics_file.stat().st_mtime
                
                if current_mtime != last_mtime:
                    mem, dur, success = load_metrics()
                    if success:
                        timestamp = time.strftime('%H:%M:%S')
                        print(f" [{timestamp}] Métriques mises à jour : Mémoire={mem:.2f} MB, Durée={dur:.2f}s")
                        last_mtime = current_mtime
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n Arrêt du serveur.")

if __name__ == "__main__":
    run_metrics_server(8001)