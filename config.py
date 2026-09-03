import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )


    if os.getenv("VERCEL"):

        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/bug_tracker.db"

    else:

        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "sqlite:///bug_tracker.db"
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )