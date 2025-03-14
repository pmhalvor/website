from flask import Flask, render_template, jsonify
from notion import CachedNotionClient, parse_about_results, parse_cv_results, parse_notes_results
from config import Env
from flask import request


env = Env(".env")         

app = Flask(__name__, static_folder='static', template_folder='templates')

NOTION_TOKEN = env.notion_sitedb_token
RADIO_URL = env.radio_url
CACHE_DIR = "./notion_cache"
CACHE_TTL = 3600

notion_client = CachedNotionClient(token=NOTION_TOKEN, cache_dir=CACHE_DIR, cache_ttl=CACHE_TTL)

@app.route('/')
def home():
    updates_data = notion_client.get_database(env.notion_sitedb_update_id)
    updates = parse_notes_results(updates_data['results'])
    return render_template('index.html', updates=updates[:7]) # most recent 7

@app.route('/updates')
def updates():
    updates_data = notion_client.get_database(env.notion_sitedb_update_id)
    updates = parse_notes_results(updates_data['results'])
    return render_template('updates.html', updates=updates)

@app.route('/about')
def about():
    about_data = notion_client.get_database(env.notion_sitedb_about_id)
    about = parse_about_results(about_data['results'])
    return render_template('about.html', about=about)

@app.route('/cv')
def cv():
    cv_data = notion_client.get_database(env.notion_sitedb_cv_id)
    cv = parse_cv_results(cv_data['results'])
    # Separate into categories like in Django views
    work = [item for item in cv if item['category'] == 'Work']
    education = [item for item in cv if item['category'] == 'Education']
    languages = [item for item in cv if item['category'] == 'Language']

    return render_template("cv.html", cv_list=cv, work_list=work, edu_list=education, lang_list=languages)


@app.route('/notes')
def notes():
    notes_data = notion_client.get_database(env.notion_sitedb_notes_id)
    notes = parse_notes_results(notes_data['results'])
    return render_template("notes.html", notes=notes)


@app.route('/rir')
def rir():
    return render_template("rir.html")


@app.route('/radio')
def radio():
    return render_template("radio.html", radio_url=RADIO_URL)


@app.route('/callback')
def callback():
    # Get the 'code' parameter from the request URL
    code = request.args.get('code')
    if code:
        return jsonify({'code': code})
    else:
        return jsonify({'error': 'No code parameter found'}), 400


if __name__ == '__main__':
    import os
    app.run(port=os.environ.get('PORT', 5001)) # TODO test other ports 
