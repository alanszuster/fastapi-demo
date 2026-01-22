from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict
import json

class Settings(BaseSettings):
    SECRET_KEY: str
    DEMO_USERS: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def get_demo_users_dict(self) -> Dict[str, str]:
        """Parse DEMO_USERS JSON string into dictionary"""
        return json.loads(self.DEMO_USERS)

settings = Settings()  # type: ignore
