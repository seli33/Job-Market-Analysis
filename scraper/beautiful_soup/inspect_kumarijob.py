import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URL = "https://www.kumarijob.com/jobs-in-nepal/ittelecommunication-jobs-in-nepal"


# ─────────────────────────────────────────────
# 1. PRINT HTML TREE (LIMITED DEPTH)
# ─────────────────────────────────────────────
def print_tree(element, indent=0, max_depth=3):
    if indent > max_depth:
        return

    name = element.name if element.name else "TEXT"
    classes = element.get("class")
    class_str = f" class={classes}" if classes else ""

    print("  " * indent + f"<{name}{class_str}>")

    for child in element.children:
        if hasattr(child, "name") and child.name is not None:
            print_tree(child, indent + 1, max_depth)


# ─────────────────────────────────────────────
# 2. INSPECT JOB CARDS
# ─────────────────────────────────────────────
def inspect_job_cards(soup, limit=3):
    cards = soup.find_all("div", class_="d-flex gap-3")

    print(f"\nFound {len(cards)} job cards\n")

    for i, card in enumerate(cards[:limit]):
        print(f"\n--- JOB CARD {i+1} ---\n")
        print(card.prettify()[:1500])  # limit output


# ─────────────────────────────────────────────
# 3. TEST SELECTORS
# ─────────────────────────────────────────────
def test_selectors(soup):
    card = soup.find("div", class_="d-flex gap-3")

    print("\n--- TESTING SELECTORS ---\n")

    # TITLE
    try:
        title = card.find("h2").text.strip()
        print("TITLE:", title)
    except:
        print("TITLE: NOT FOUND")

    # URL
    try:
        url = card.find("h2").find("a")["href"]
        print("URL:", url)
    except:
        print("URL: NOT FOUND")

    # COMPANY
    try:
        company = card.find("a", class_="link-route").text.strip()
        print("COMPANY:", company)
    except:
        print("COMPANY: NOT FOUND")

    # LOCATION
    try:
        location = card.find("span", class_="district-text").text.strip()
        print("LOCATION:", location)
    except:
        print("LOCATION: NOT FOUND")

    return url if 'url' in locals() else None


# ─────────────────────────────────────────────
# 4. INSPECT DETAIL PAGE
# ─────────────────────────────────────────────
def inspect_detail_page(url):
    if not url:
        print("\nNo valid job URL to inspect.")
        return

    # Fix relative URL
    if url.startswith("/"):
        url = "https://www.kumarijob.com" + url

    print(f"\nInspecting detail page: {url}\n")

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    print("\n--- DETAIL PAGE HTML PREVIEW ---\n")
    print(soup.prettify()[:2000])


# ─────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────
if __name__ == "__main__":
    response = requests.get(URL, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch page")
        exit()

    soup = BeautifulSoup(response.text, "html.parser")

    print("\n==============================")
    print("1. PAGE STRUCTURE (LIMITED)")
    print("==============================\n")
    print_tree(soup.body, max_depth=3)

    print("\n==============================")
    print("2. JOB CARD STRUCTURE")
    print("==============================")
    inspect_job_cards(soup)

    print("\n==============================")
    print("3. SELECTOR TEST")
    print("==============================")
    job_url = test_selectors(soup)

    print("\n==============================")
    print("4. DETAIL PAGE STRUCTURE")
    print("==============================")
    inspect_detail_page(job_url)