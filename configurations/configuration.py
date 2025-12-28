from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

class Settings(BaseSettings):
    open_agenda_api_url: HttpUrl = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/evenements-publics-openagenda/records/"
    open_agenda_api_limit: int = 100
    open_agenda_api_offset: int = 0
    base_dir: Path = Path(__file__).resolve().parent
    mistral_api_key: str = ""

    mistral_chatbot_limit_tokens: int = 500
    mistral_chatbot_top_p: float = 0.9
    mistral_chatbot_temperature: float = 0.7
    mistral_chatbot_max_messages_history: int = 10

    input_dir: Path = base_dir / "inputs"
    output_dir: Path = base_dir / "outputs"
    json_filename: str = "evenements-publics-openagenda.json"
    json_filename_clean: str = "evenements-publics-openagenda-clean.json"
    txt_filename: str = "evenements.txt"
    faiss_index_mistral: str = "faiss_index_mistral"

    @property
    def json_full_path(self) -> Path:
        """Retourne le chemin complet du fichier JSON."""
        return self.input_dir / self.json_filename
    
    @property
    def json_clean_full_path(self) -> Path:
        """Retourne le chemin complet du fichier JSON Clean."""
        return self.output_dir / self.json_filename_clean

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" 
    )

settings = Settings()
