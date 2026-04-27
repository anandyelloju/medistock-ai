import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized configuration management for MediStock AI.
    Handles environment-specific settings and secure credentials.
    """
    # Environment Mode
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = ENV == "development"

    # API Credentials
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Email / SMTP Settings
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    SUPPLIER_EMAIL = os.getenv("SUPPLIER_EMAIL")

    # Database Settings
    DB_PATH = os.getenv("DB_PATH", "database/inventory.db")

    @classmethod
    def validate(cls):
        """Ensures critical configuration is present."""
        missing = []
        if not cls.GROQ_API_KEY: missing.append("GROQ_API_KEY")
        if not cls.SMTP_USER: missing.append("SMTP_USER")
        if not cls.SMTP_PASS: missing.append("SMTP_PASS")
        
        if missing and cls.ENV == "production":
            raise ValueError(f"Missing critical production environment variables: {', '.join(missing)}")
        return True

# Initialize and validate
Config.validate()
