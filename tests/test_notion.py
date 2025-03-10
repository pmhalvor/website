from home.notion import CachedNotionClient
from home.config import Env
import pytest

env = Env(".env")


@pytest.mark.skip(reason="Notion API key required")
def test_get_database():
    notion_client = CachedNotionClient(token=env.notion_sitedb_token, cache_dir="./notion_cache", cache_ttl=3600)
    database_data = notion_client.get_database(env.notion_sitedb_update_id)

    assert database_data is not None
    assert "results" in database_data
