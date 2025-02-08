from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    UNISWAP_API_KEY: str = os.getenv("UNISWAP_API_KEY")


# Singleton settings instance
settings = Settings()