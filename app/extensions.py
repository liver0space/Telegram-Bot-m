import logging
import coloredlogs

from flask_bootstrap import Bootstrap5
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG', logger=logger, isatty=True)

db = SQLAlchemy()
bootstrap = Bootstrap5()
socketio = SocketIO()