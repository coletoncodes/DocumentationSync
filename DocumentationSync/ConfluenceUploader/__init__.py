# __init__.py
from requests.auth import HTTPBasicAuth
from ConfluenceUploader.config import Config

# Initialize this class with the Config values.
# def __init__(self):
#     self._AUTH = HTTPBasicAuth(
#         Config.CONFLUENCE_EMAIL,
#         Config.CONFLUENCE_API_KEY
#     )

    # self._HEADERS = {
    #     "Accept": "application/json",
    #     "Content-Type": "application/json"
    # }