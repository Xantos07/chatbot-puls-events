from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

class Settings(BaseSettings):
    api_url: HttpUrl = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/evenements-publics-openagenda/records/"
    api_limit: int = 100
    api_offset: int = 0
    base_dir: Path = Path(__file__).resolve().parent
    
    input_dir: Path = base_dir / "inputs"
    output_dir: Path = base_dir / "outputs"
    json_filename: str = "evenements-publics-openagenda.json"

    @property
    def json_full_path(self) -> Path:
        """Retourne le chemin complet du fichier JSON."""
        return self.input_dir / self.json_filename

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" 
    )

settings = Settings()
