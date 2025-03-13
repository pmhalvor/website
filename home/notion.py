import time
import json
import os
from notion_client import Client
from datetime import datetime
import pandas as pd

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


def parse_about_results(results):
    """
    Identifier: Name
    Content: Text
    """
    parsed_results = []
    for result in results:
        parsed_result = {
            'title': result['properties']['Name']['title'][0]['text']['content'],
            'content': [line.get("plain_text") for line in result['properties']['Text']['rich_text']]
        }
        parsed_results.append(parsed_result)
    
    # reverse order to show most recent first
    return parsed_results[::-1]


def parse_cv_results(results):
    """
    Identifier: Name
    Fields:
        category
        title
        subtitle
        location
        start_date
        end_date
    """

    parsed_results = []
    for result in results:

        parsed_result = {
            'id': result['properties']['Name']['title'][0]['text']['content'],
            'category': result['properties']['category']['select']['name'],
            'title': result['properties']['title']['rich_text'][0]['text']['content'],
            'subtitle': extract_optional_text(result, 'subtitle'),
            'location': extract_optional_text(result, 'location'),
            'start_date': extract_date(result, 'start'),
            'end_date': extract_date(result, 'end')
        }
        parsed_results.append(parsed_result)

    # convert to pandas, sort by start date and convert back to list
    df = pd.DataFrame(parsed_results)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    df = df.sort_values(by='start_date', ascending=False)

    df['duration'] = round((df['end_date'] - df['start_date']).dt.days / 365, 1) # calculate duration in years

    # convert dates to readable format
    df['start_date'] = df['start_date'].dt.strftime('%b %Y')
    df['end_date'] = df['end_date'].dt.strftime('%b %Y')
    df = df.fillna('')

    parsed_results = df.to_dict(orient='records')

    return parsed_results


def parse_notes_results(results):
    """
    Parse content populating Notes and Updates sections

    Identifier: Name
    Fields:
        title
        description
        publish_date
        file
        image
        tags
    """
    parsed_results = []

    for result in results:
        parsed_result = {
            'id': result['properties']['Name']['title'][0]['text']['content'],
            'title': result['properties']['title']['rich_text'][0]['text']['content'],
            'description': result['properties']['description']['rich_text'][0]['text']['content'],
            'publish_date': extract_date(result, 'start'),
            'file': extract_url(result, 'file'),
            'image': extract_url(result, 'image'),
            'tags': [tag['name'] for tag in result['properties']['tags']['multi_select']]
        }
        parsed_results.append(parsed_result)


    parsed_results = order_by(parsed_results, 'publish_date', reverse=True)

    return parsed_results


# utils 
def pp(content):
    print(json.dumps(content, indent=2))

def order_by(results, key, reverse=True):
    return sorted(results, key=lambda x: x[key], reverse=reverse)


def extract_optional_text(result, key):
    value = result['properties'][key].get("rich_text", [])
    if len(value) > 0:
        return value[0]['plain_text']
    return ""


def extract_date(result, key):
    value = result['properties']['date']['date'].get(key)
    if value is None:
        return datetime.now().isoformat(timespec='seconds')
    return datetime.strptime(value, "%Y-%m-%d").isoformat()


def extract_url(result, key):
    value = result['properties'][key].get("files", [])
    if len(value) > 0:
        if 'external' in value[0]:
            return value[0]['external']['url']
        return value[0]['file']['url']
    return ""   


if __name__ == "__main__":
    from config import Env

    env = Env(".env")

    sdb_client = CachedNotionClient(env.notion_sitedb_token)

    about_data = sdb_client.get_database(env.notion_sitedb_about_id)
    cv_data = sdb_client.get_database(env.notion_sitedb_cv_id)
    notes_data = sdb_client.get_database(env.notion_sitedb_notes_id)
    updates_data = sdb_client.get_database(env.notion_sitedb_update_id)

    pp(parse_about_results(about_data['results']))
    pp(parse_cv_results(cv_data['results']))
    pp(parse_notes_results(notes_data['results']))
    pp(parse_notes_results(updates_data['results']))
    
    print("Done.")