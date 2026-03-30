"""
scraper/scrape_linkedin.py
LinkedIn Jobs Scraper — Dynamic Scraping with Selenium + BeautifulSoup
 
Demonstrates:
  - Selenium WebDriver setup with anti-detection options
  - Infinite scroll handling via JavaScript execution
  - 'See more jobs' button click automation
  - BeautifulSoup parsing of dynamically loaded HTML
  - Structured data extraction to CSV (matches project's jobs schema)
 
NOTE: For educational/portfolio purposes only.
      Respect LinkedIn's ToS and use rate limiting.
"""

import time
import random 
import csv
import os
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




from bs4 import BeautifulSoup