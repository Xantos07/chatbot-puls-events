import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from builder.open_agenda import build_where
from configurations.configuration import settings
from datetime import datetime
import requests


def fetch_events(region, date_start, date_end, limit=10):
    """Fonction helper pour récupérer des événements"""
    url = str(settings.open_agenda_api_url)
    params = {
        "limit": limit,
        "offset": 0,
        "where": build_where(region, date_start, date_end)
    }
    response = requests.get(url, params=params)
    assert response.status_code == 200
    return response.json().get("results", [])


def test_build_where():
    """Test de la fonction build_where"""
    result = build_where("Hauts-de-France", "2024-12-01", "2025-12-31")
    expected = "location_region = 'Hauts-de-France' AND firstdate_begin >= '2024-12-01' AND firstdate_begin <= '2025-12-31'"
    assert result == expected


def test_api_returns_valid_events():
    """Test que l'API retourne des événements valides dans la bonne région et période"""
    events = fetch_events("Hauts-de-France", "2024-12-01", "2025-12-31")
    
    assert len(events) > 0, "Aucun événement retourné"
    
    start = datetime.fromisoformat("2024-12-01")
    end = datetime.fromisoformat("2025-12-31T23:59:59")
    
    for event in events:
        event_date = datetime.fromisoformat(event["firstdate_begin"].replace('+00:00', ''))
        assert start <= event_date <= end, f"Date hors plage: {event_date}"
        assert event["location_region"] == "Hauts-de-France"


def test_api_no_events_for_invalid_region():
    """Test qu'une région inexistante retourne 0 événements"""
    events = fetch_events("RégionInexistante", "2024-12-01", "2025-12-31")
    assert len(events) == 0