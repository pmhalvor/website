from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Env(BaseSettings):
    notion_database_id: str = Field(..., env='NOTION_DATABASE_ID', title='Notion Database ID')
    notion_token: str = Field(..., env='NOTION_TOKEN', title='Notion Token')
    root: str = Field(..., env='ROOT', title='Root path')
    spotify_client_id: str = Field(..., env='SPOTIFY_CLIENT_ID', title='Spotify Client ID')
    spotify_client_secret: str = Field(..., env='SPOTIFY_CLIENT_SECRET', title='Spotify Client Secret')

    def __init__(self, env_file: str = ".env", **kwargs):
        load_dotenv(env_file)
        super().__init__(**kwargs)

if __name__ == "__main__":
    env = Env()
    
    print(f"Notion token:       {env.notion_token[:5]}...")
    print(f"Notion database id: {env.notion_database_id[:5]}...")
    print(f"Spotify client id:  {env.spotify_client_id[:5]}...")