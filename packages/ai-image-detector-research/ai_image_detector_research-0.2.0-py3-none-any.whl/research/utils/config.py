from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME", "")
    KAGGLE_KEY = os.getenv("KAGGLE_KEY", "")

    if not KAGGLE_USERNAME or not KAGGLE_KEY:
        raise ValueError(
            "KAGGLE_USERNAME and KAGGLE_KEY must be set in the environment variables."
        )
