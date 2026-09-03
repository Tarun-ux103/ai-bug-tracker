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


if database_url:

    # Some PostgreSQL providers use postgres://
    # SQLAlchemy prefers postgresql://
    if database_url.startswith("postgres://"):

        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )


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
    else "NO DATABASE URL"
)


class Config:

    SECRET_KEY = (
        secret_key
        if secret_key
        else "development-secret-key"
    )


    # Use DATABASE_URL from Neon/Vercel
    SQLALCHEMY_DATABASE_URI = database_url


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
        ""
    ).strip()