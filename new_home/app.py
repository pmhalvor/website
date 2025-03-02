from flask import Flask, render_template
from notion import CachedNotionClient
from config import Env
from flask import request

env = Env() # use when running python app.py
# env = Env("new_home/.env") # use when running python new_home/app.py

app = Flask(__name__, static_folder='static', template_folder='templates')

NOTION_TOKEN = env.notion_token
DATABASE_ID = env.notion_database_id
CACHE_DIR = "./notion_cache"
CACHE_TTL = 3600

notion_client = CachedNotionClient(token=NOTION_TOKEN, cache_dir=CACHE_DIR, cache_ttl=CACHE_TTL)

@app.route('/rir')
def rir():
    try:
        database_data = notion_client.get_database(DATABASE_ID)
        items = database_data['results'] if 'results' in database_data else []
    except Exception as e:
        items = []
        print(f"Error fetching data from Notion: {e}")

    # Pagination logic
    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = items[start:end]

    return render_template("index.html", items=paginated_items, page=page)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  
