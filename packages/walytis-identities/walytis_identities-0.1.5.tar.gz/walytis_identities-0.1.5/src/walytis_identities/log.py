import logging
from logging.handlers import RotatingFileHandler
import os

LOG_PATH = ".walytis_identities.log"
print(f"Logging to {os.path.abspath(LOG_PATH)}")

# Formatter
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Console handler (INFO+)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# File handler (DEBUG+ with rotation)
file_handler = RotatingFileHandler(
    LOG_PATH, maxBytes=5*1024*1024, backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# # Root logger
# logger_root = logging.getLogger()
# logger_root.setLevel(logging.DEBUG)  # Global default
# logger_root.addHandler(console_handler)
# # logger_root.addHandler(file_handler)

logger_walid = logging.getLogger("WalId")
logger_walid.setLevel(logging.INFO)
logger_walid.addHandler(file_handler)
logger_walid.addHandler(console_handler)

logger_dm = logging.getLogger("WalId.DM")
logger_dm.setLevel(logging.INFO)
logger_dm.addHandler(file_handler)
logger_dm.addHandler(console_handler)


logger_gdm = logging.getLogger("WalId.GDM")
logger_gdm.setLevel(logging.INFO)
logger_gdm.addHandler(file_handler)
logger_gdm.addHandler(console_handler)

logger_dmws = logging.getLogger("WalId.DMWS")
logger_dmws.setLevel(logging.INFO)
logger_dmws.addHandler(file_handler)
logger_dmws.addHandler(console_handler)
