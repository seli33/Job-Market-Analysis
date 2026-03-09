import requests
from bs4 import BeautifulSoup

HEADERS={
    "USER-AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def inspect():
    url="https://www.kumarijob.com/search"
    response=requests.get(url,headers=HEADERS)

    print("status code :",response.status_code)
    print("="*50)

