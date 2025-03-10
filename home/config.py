from dotenv import load_dotenv
import os

class Env:
    def __init__(self, env_file: str = ".env"):
        load_dotenv(env_file)
        self.env_vars = {key.lower(): value for key, value in os.environ.items()}
        print("Found env vars:", self.env_vars)

    def __getattr__(self, item):
        try:
            return self.env_vars[item]
        except KeyError:
            raise AttributeError(f"'Env' object has no attribute '{item}'")


if __name__ == "__main__":
    env = Env("new_home/.env")
    N = 5
    
    print(f"Notion token:        {env.notion_token[:N]}...")
    print(f"Notion database id:  {env.notion_database_id[:N]}...")
    print(f"Notion SiteDB token: {env.notion_sitedb_token[:N]}...")
    print(f"Notion SiteDB about: {env.notion_sitedb_about_id[:N]}...")
    print(f"Notion SiteDB cv:    {env.notion_sitedb_cv_id[:N]}...")

    print(f"Spotify client id:   {env.spotify_client_id[:N]}...")