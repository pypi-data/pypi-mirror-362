import requests

from .bc2pg import bc2pg as bc2pg
from .bcdc import get_table_definition as get_table_definition
from .bcdc import get_table_name as get_table_name
from .wfs import get_count as get_count
from .wfs import get_data as get_data
from .wfs import get_sortkey as get_sortkey
from .wfs import list_tables as list_tables
from .wfs import validate_name as validate_name

PRIMARY_KEY_DB_URL = "https://raw.githubusercontent.com/smnorris/bcdata/main/data/primary_keys.json"

# BCDC does not indicate which column in the schema is the primary key.
# In this absence, bcdata maintains its own dictionary of {table: primary_key},
# served via github. Retrieve the dict with this function"""
response = requests.get(PRIMARY_KEY_DB_URL)
if response.status_code == 200:
    primary_keys = response.json()
else:
    raise Exception(f"Failed to download primary key database at {PRIMARY_KEY_DB_URL}")
    primary_keys = {}

__version__ = "0.16.0post1"
