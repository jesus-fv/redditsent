from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str

    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()