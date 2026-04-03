import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.kumarijob.com/jobs-in-nepal/ittelecommunication-jobs-in-nepal"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Test new selector
job_cards = soup.find_all("h2", class_=["mb-0", "fw-semibold"])
print(f"Jobs found: {len(job_cards)}")

for card in job_cards[:5]:
    print(" -", card.text.strip())
    
    # Look at what's inside parent div
    parent = card.find_parent("div")
    print("   Parent HTML:")
    print(parent.prettify()[:300])
    print()

print("grandparent structure")
card=job_cards[0]
parent      = card.find_parent("div")        # one level up
grandparent = parent.find_parent("div")      # two levels up
great_grand = grandparent.find_parent("div") # three levels up

print("=== PARENT ===")
print(parent.prettify()[:500])

print("=== GRANDPARENT ===")
print(grandparent.prettify()[:800])

print("\n=== GREAT GRANDPARENT ===")
print(great_grand.prettify()[:1200])