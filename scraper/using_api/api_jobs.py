import http.client

conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "e51d01b32cmsh674326f8bee47f1p1ffff7jsn6dd5a5082d78",
    'x-rapidapi-host': "jsearch.p.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("GET", "/search?query=developer%20jobs%20in%20chicago&page=1&num_pages=1&country=us&date_posted=all", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))