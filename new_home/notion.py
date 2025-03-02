import time
import json
import os
from notion_client import Client

class NotionDatabase:
    def __init__(self, token, database_id):
        self.notion = Client(auth=token)
        self.database_id = database_id
        
    def get_all_items(self):
        response = self.notion.databases.query(database_id=self.database_id)
        return response["results"]
        
    def get_item(self, page_id):
        return self.notion.pages.retrieve(page_id=page_id)
        
    # Additional CRUD methods as needed



class CachedNotionClient:
    def __init__(self, token, cache_dir='./notion_cache', cache_ttl=3600):
        self.notion = Client(auth=token)
        self.cache_dir = cache_dir
        self.cache_ttl = cache_ttl  # Time-to-live in seconds
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def _read_cache(self, key):
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
            
        # Check if cache is expired
        if time.time() - os.path.getmtime(cache_path) > self.cache_ttl:
            return None
            
        try:
            with open(cache_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def _write_cache(self, key, data):
        with open(self._get_cache_path(key), 'w') as f:
            json.dump(data, f)
    
    def get_database(self, database_id):
        cache_key = f"db_{database_id}"
            
        try:
            data = self.notion.databases.query(database_id=database_id)
            self._write_cache(cache_key, data)
            return data
        except Exception as e:
            # If Notion API fails, return last cached version even if expired
            last_cache = self._read_cache(cache_key)
            if last_cache:
                return last_cache
            raise e
            
    # Add additional methods for other Notion API calls
