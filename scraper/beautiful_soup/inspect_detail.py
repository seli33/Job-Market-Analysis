import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

BASE_URL = "https://www.kumarijob.com"


def get_detail_url():
    listing="https://www.kumarijob.com/jobs-in-nepal/ittelecommunication-jobs-in-nepal"
    r=requests.get(listing,headers=HEADERS)
    soup=BeautifulSoup(r.text,"html.parser")

    for h2 in soup.find_all("h2",class_="mb-0"):
        a=h2.find("a")
        if a and a.get("href"):
            href=a["href"]
            if not href.startswith("http"):
                href= BASE_URL + href
            return href
    return None

def inspect_detail(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    print(f"Status: {r.status_code}")
    print(f"URL: {url}")
    print("=" * 60)

    print("\n--- DIV CLASSES ---")
    for div in soup.find_all("div", class_=True)[:50]:
        print(div.get("class"))

    print("\n--- TABLE ROWS ---")
    for row in soup.find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
        if cells:
            print(" | ".join(cells))

    print("\n--- LABEL-LIKE TEXT ---")
    seen = set()
    for tag in soup.find_all(["span", "strong", "td", "li", "p"]):
        txt = tag.get_text(strip=True)
        if ":" in txt and 5 < len(txt) < 100 and txt not in seen:
            seen.add(txt)
            print(f"  <{tag.name}>  {txt}")

    print("\n--- ALL P TAGS ---")
    for p in soup.find_all("p"):
        txt = p.get_text(strip=True)
        if txt:
            print(f"  {txt[:100]}")

    print("\n--- ALL HEADINGS ---")
    for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        print(f"  {tag.name} | {tag.get_text(strip=True)[:80]}")


if __name__ == "__main__":
    print("Getting detail URL from listing page...")
    url = get_detail_url()

    if url:
        print(f"Found: {url}\n")
        inspect_detail(url)
    else:
        print("Could not find a job URL.")