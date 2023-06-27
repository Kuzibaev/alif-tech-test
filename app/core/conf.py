import os
from pathlib import Path
from typing import Any

import pytz
from pydantic import BaseSettings, validator, PostgresDsn

APP_DIR = Path(__file__).parent.parent
BASE_DIR = APP_DIR.parent
DEBUG = os.getenv('DEBUG', 'True') == 'True'


class Settings(BaseSettings):
    # Project Config
    PROJECT_NAME: str = 'Alif Tech Test Project'
    SECRET_KEY: str = 'secret-key'

    # DB Config
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_CONFIG: str = ''

    DEBUG: bool = DEBUG

    # SMTP service
    SMTP_SERVER: str = ''
    SENDER_EMAIL: str = ''
    SENDER_PASSWORD: str = ''

    # TWILIO
    ACCOUNT_SID: str = ''
    AUTH_TOKEN: str = ''
    TWILIO_NUMBER: str = ''

    # Timezone
    TIMEZONE: str = 'Asia/Tashkent'

    def get_project_name(self):
        return self.PROJECT_NAME.lower().replace(' ', '_').replace("-", "_")

    def get_project_slug(self):
        return self.PROJECT_NAME.lower().replace(' ', '-').replace('_', '-')

    timezone: Any = pytz.timezone(TIMEZONE)

    @validator('DB_CONFIG')
    def db_config(cls, _, values: dict):
        return PostgresDsn.build(
            scheme='postgresql+psycopg2',
            user=values['DB_USER'],
            password=values['DB_PASSWORD'],
            host=values['DB_HOST'],
            port=str(values['DB_PORT']),
            path=f"/{values['DB_NAME']}"

        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
