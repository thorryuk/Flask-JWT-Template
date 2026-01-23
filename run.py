import os
from app import create_app
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / '.env', override=True)
dotenv_path = BASE_DIR / "environment" / f".env.{os.getenv('APP_ENV')}"
load_dotenv(dotenv_path=dotenv_path, override=True)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
