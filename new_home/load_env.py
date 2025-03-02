import os
from dotenv import load_dotenv

def load_env(path=None, verbose=False):
    load_dotenv(path, verbose=verbose)

    check_var('DJANGO_SECRET')
    check_var('NOTION_TOKEN')

    return os.environ


def check_var(var):
    if not os.environ.get(var):
        print(
            f"Warning: {var} not set in environment." \
            "Consider passing path to .env, like: new_home/.env"
        )
        return False
    return True


if __name__ == "__main__":
    load_env()
