import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from datetime import datetime

HEADERS={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
}

CATEGORIES={
    "marketing":        "marketing-sales-jobs-in-nepal",
    "customer_service": "customer-service-jobs-in-nepal",
    "education":        "education-jobs-in-nepal",
    "digital_marketing":"digital-marketing-jobs-in-nepal",
    "accounting":       "accounting-and-finance-jobs-in-nepal",
    "it":               "ittelecommunication-jobs-in-nepal",
    "hospitality":      "hospitality-jobs-in-nepal",
    "engineering":      "engineering-jobs-in-nepal",
    "content_writing":  "content-writer-content-editor-jobs-in-nepal",
    "fullstack":        "full-stack-development-jobs-in-nepal",
}
response=requests.get(url,headers=HEADERS,timeout=10)

if response.status_code != 200:
    print(f"Failed:{response.status_code}")
    
