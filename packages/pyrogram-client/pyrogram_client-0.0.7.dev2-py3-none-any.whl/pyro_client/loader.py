from dotenv import load_dotenv
from os import getenv as env

from x_auth import models

load_dotenv()

API_ID = env("API_ID")
API_HASH = env("API_HASH")
PG_DSN = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST', 'xyncdbs')}:" \
         f"{env('POSTGRES_PORT', 5432)}/{env('POSTGRES_DB', env('POSTGRES_USER'))}"
TORM = {
    "connections": {"default": PG_DSN},
    "apps": {"models": {"models": [models]}},
    "use_tz": False,
    "timezone": "UTC",
}
TOKEN = env("TOKEN")
WSToken = env("WST")
