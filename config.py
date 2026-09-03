import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


database_url = os.getenv(
    "DATABASE_URL",
    ""
).strip()


secret_key = os.getenv(
    "SECRET_KEY",
    ""
).strip()


# Safe diagnostics for Vercel logs
# These do NOT print secret values

print(
    "DATABASE_URL found:",
    bool(database_url)
)

print(
    "Database type:",
    database_url.split(":", 1)[0]
    if database_url
    else "SQLite fallback"
)

print(
    "SECRET_KEY found:",
    bool(secret_key)
)


class Config:

    SECRET_KEY = (
        secret_key
        if secret_key
        else "development-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        database_url
        if database_url
        else f"sqlite:///{os.path.join(BASE_DIR, 'bug_tracker.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )