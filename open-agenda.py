import requests
import json
from configuration import settings  


def main():
    url = str(settings.api_url)

    print(f"-------------------------")
    print(f"Cible : {url}")
    print(f"Destination : {settings.json_full_path}")
    print(f"-------------------------")

    all_rows = []
    offset = 0
    limit = settings.api_limit

    try:
        # obtenir le total
        # "location_region = 'Hauts-de-France' "
        # seulement 1 an
        params = {
            "limit": limit,
            "offset": 0,
            "where": (
                "location_region = 'Hauts-de-France' "
                "AND firstdate_begin >= '2024-12-01' "
                "AND firstdate_begin <= '2025-12-31' "

            )
        }

        print("Récupération des données")
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        total_count = data.get("total_count", 0)
        rows = data.get("results", [])
        all_rows.extend(rows)

        print(f"-- Total à récupérer : {total_count} lignes")
        print(f"-- Page 1 : {len(rows)} lignes récupérées")

        # Boucle pour les données pages suivantes
        page = 2
        while len(all_rows) < total_count:
            offset += limit
            
            params = {
                "limit": limit,
                "offset": offset,
                "where": (
                    "location_region = 'Hauts-de-France' "
                    "AND firstdate_begin >= '2024-12-01' "
                    "AND firstdate_begin <= '2025-12-31' "
                )
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            rows = data.get("results", [])

            if not rows:
                break

            # ram 
            all_rows.extend(rows)
            print(f"-- Page {page} : {len(rows)} lignes (total: {len(all_rows)}/{total_count})")
            
            page += 1

        # enregistrer le fichier 
        with open(settings.json_full_path, 'w', encoding='utf-8') as f:
            json.dump(all_rows, f, indent=4, ensure_ascii=False)

        print("-------------------------")
        print(f"Fichier sauvegardé : {settings.json_full_path}")
        print(f"Lignes totales : {len(all_rows)}/{total_count}")
        print("-------------------------")

    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau : {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Code HTTP : {e.response.status_code}")
            print(f"   Message : {e.response.text[:500]}")
    except json.JSONDecodeError as e:
        print(f" Erreur JSON : {e}")
    except IOError as e:
        print(f" Erreur fichier : {e}")


if __name__ == "__main__":
    main()
