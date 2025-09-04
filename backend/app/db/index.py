from pathlib import Path
from dotenv import load_dotenv
from prisma import Prisma

# Load .env that lives alongside this file (backend/app/db/.env)
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

prisma = Prisma()