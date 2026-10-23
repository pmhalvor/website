# perhalvorsen.com 
Repository for my personal website, [perhalvorsen.com](https://perhalvorsen.com).

Changes are pushed to ghcr.io/pmhavor/website (PAT needed).
On my server, I use [watchtower](https://containrrr.dev/watchtower/) to automatically update the site when a new image is pushed to the registry.


I use this site as a portfolio, 
showcasing some of the web-development projects I've taken part in.
If you noticed anything wrong, feel free to open a PR.

## Changelog:
- 3.0.0: Refactor Django -> Flask, postgres -> Notion, plus Dockerized (see inital update in [#13](https://github.com/pmhalvor/website/pull/13) and Django removal in [#14](https://github.com/pmhalvor/website/pull/14))
- 2.1.0: Updated server to Ubuntu 4.23 and ensure environment vars present
- 2.0.0: Migrated off of Azure. Everything is now soley hosted on Digial Ocean server
- 1.1.4: current, recents, and plots loaded seperately from `/radio`, allowing for smoother user experience
- 1.1.3: Radio branch now serving data locally for fewer server timeouts on page refresh
- 1.1.2: Radio branch now has plots showing data from Azure storage
- 1.1.1: Radio branch incorperating calls to the [Spotify API](developers.spotify.com)
- 1.0.5: Code stored in database on server. Items served dynamically using Django.
- 1.0.4: Notes stored in database on server. Page items are pulled dynamically using Django.
- 1.0.3: Home page updates stored in database on server. Items pulled dynamically from Django.
- 1.0.2: Cv entries stored in database. Served dynamically using Django.
- 1.0.1: Static site from previous deploy hosted from server.


# Useful commands when developing

## Run site container
Uses `docker compose` to build, run, then tear down the site container. 
```sh
make run
```

## Manual rebuild
```sh
docker compose build home && docker kill home && docker compose up home -d
```

## Run locally for development
Navigate to `new_home/` and run the app:
```sh
cd new_home/
python app.py
``` 
Ensure you have a `.env` file with your Notion credentials:
- `NOTION_SITEDB_TOKEN`
- `NOTION_SITEDB_ID`
