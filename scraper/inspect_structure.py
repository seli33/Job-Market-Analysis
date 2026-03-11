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

job_cards = soup.find_all("h2", class_=["mb-0", "fw-semibold"])
card = job_cards[0]

# Navigate to great grandparent - that's the full job card
great_grand = card.find_parent("div") \
                  .find_parent("div") \
                  .find_parent("div")

# Print the FULL great grandparent - no character limit
print(great_grand.prettify())