from new_home.notion import CachedNotionClient
from new_home.load_env import load_env

env = load_env()


def test_get_database():
    notion_client = CachedNotionClient(token=env.get("NOTION_TOKEN"), cache_dir="./notion_cache", cache_ttl=3600)
    database_data = notion_client.get_database(env.get("DATABASE_ID"))

    assert database_data is not None
    assert "results" in database_data