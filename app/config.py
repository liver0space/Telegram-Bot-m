import os 
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{POSTGRES_PASSWORD}@postgreDB:5432/my_dbase"
    ALLOWED_ADMINS = os.environ.get('ALLOWED_ADMINS', '')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')