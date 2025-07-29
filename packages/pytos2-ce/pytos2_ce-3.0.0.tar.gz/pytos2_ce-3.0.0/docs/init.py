from dotenv import dotenv_values
from pytos2.secureapp import Sa as SecureApp
from pytos2.securechange import Scw as SecureChange
from pytos2.securetrack import St as SecureTrack
from helpers import pp, pretty, ugly, pretty_json, ugly_json


# Loads our config
config = dotenv_values(".env")

# Override or Use Config Values (Strings must be empty to use config - any value in string will be truthy)
HOST = "" or config["HOST"]
USER = "" or config["USER"]
PASS = "" or config["PASS"]

# Instantiate Classes
secure_app = SecureApp(HOST, USER, PASS)
secure_change = SecureChange(HOST, USER, PASS)
secure_track = SecureTrack(HOST, USER, PASS)
