import os

from dotenv import load_dotenv

from app import create_app
from config import Config

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

app = create_app()

