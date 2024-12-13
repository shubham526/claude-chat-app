import os
from dotenv import load_dotenv
import tempfile

load_dotenv()


class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-key-please-change')

    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = tempfile.gettempdir()
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

    # Security Headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
