from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    open_agenda_api_url: HttpUrl = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/evenements-publics-openagenda/records/"
    open_agenda_api_limit: int = 100
    open_agenda_api_offset: int = 0
    
    mistral_api_key: str = ""

    mistral_chatbot_limit_tokens: int = 500
    mistral_chatbot_top_p: float = 0.9
    mistral_chatbot_temperature: float = 0.7
    mistral_chatbot_max_messages_history: int = 10

    json_filename: str = "evenements-publics-openagenda.json"
    json_filename_clean: str = "evenements-publics-openagenda-clean.json"
    txt_filename: str = "evenements.txt"
    faiss_index_mistral: str = "faiss_index_mistral"

    @property
    def base_dir(self) -> Path:
        """Retourne le répertoire racine du projet."""
        return PROJECT_ROOT
    
    @property
    def input_dir(self) -> Path:
        """Retourne le répertoire des fichiers d'entrée."""
        return PROJECT_ROOT / "inputs"
    
    @property
    def output_dir(self) -> Path:
        """Retourne le répertoire des fichiers de sortie."""
        return PROJECT_ROOT / "outputs"

    @property
    def json_full_path(self) -> Path:
        """Retourne le chemin complet du fichier JSON."""
        return self.input_dir / self.json_filename
    
    @property
    def json_clean_full_path(self) -> Path:
        """Retourne le chemin complet du fichier JSON Clean."""
        return self.output_dir / self.json_filename_clean

    @property
    def txt_full_path(self) -> Path:
        """Retourne le chemin complet du fichier TXT."""
        return self.output_dir / self.txt_filename
    
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore" 
    )

settings = Settings()