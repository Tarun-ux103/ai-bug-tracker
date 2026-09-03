import os

from dotenv import load_dotenv


# Load environment variables from .env during local development
load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# Get environment variables
database_url = os.getenv(
    "DATABASE_URL",
    ""
).strip()

secret_key = os.getenv(
    "SECRET_KEY",
    ""
).strip()


# Safe diagnostics
# These do NOT reveal actual secret values

print(
    "DATABASE_URL found:",
    bool(database_url)
)

print(
    "Database type:",
    database_url.split(
        ":",
        1
    )[0]
    if database_url
    else "SQLite fallback"
)

print(
    "SECRET_KEY found:",
    bool(secret_key)
)


class Config:

    # Secret key
    SECRET_KEY = (
        secret_key
        if secret_key
        else "development-secret-key"
    )


    # Database configuration

    # Use Neon PostgreSQL when DATABASE_URL exists.
    # Use SQLite only for local development.

    SQLALCHEMY_DATABASE_URI = (
        database_url
        if database_url
        else f"sqlite:///{os.path.join(
            BASE_DIR,
            'bug_tracker.db'
        )}"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Groq API key

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
        ""
    ).strip()