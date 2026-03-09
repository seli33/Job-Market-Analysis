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

    soup=BeautifulSoup(response.text,"html.parser")

    print("page title:",soup.title.text if soup.title else "No title" )
    print("="*50)
    
    # Print all divs with classes - this reveals job card structure
    print("\n--- DIV CLASS NAMES (first 40) ---")
    for div in soup.find_all("div", class_=True)[:40]:
        print(div.get("class"))
    
    print("\n--- ALL ANCHOR TAGS WITH HREF (first 20) ---")
    for a in soup.find_all("a", href=True)[:20]:
        print(a.get("href"), "|", a.text.strip()[:50])
    
    print("\n--- H1, H2, H3 TAGS ---")
    for tag in soup.find_all(["h1", "h2", "h3"])[:20]:
        print(tag.name, "|", tag.get("class"), "|", tag.text.strip()[:60])

if __name__ == "__main__":
    inspect()

