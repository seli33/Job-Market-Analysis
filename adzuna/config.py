import os
from dotenv import load_dotenv
import requests
import json
import pandas as pd
from config import APP_ID ,APP_KEY

load_dotenv()
APP_ID=os.getenv("ADZUNA_APP_ID")
APP_KEY=os.getenv("ADZUNA_APP_KEY")

