from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_duckduckgo(query, max_results=40):
    try:
        session = requests.Session()
        headers = {"User-Agent":"Mozilla/5.0"}
        url = "https://html.duckduckgo.com/html/"
        data = {"q": query}
        response = session.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,"html.parser")
        results=[]
        for r in soup.find_all("div", class_="result", limit=max_results):
            link_tag=r.find("a", class_="result__a")
            snippet_tag=r.find("a", class_="result__snippet")
            if link_tag:
                results.append({
                    "title": link_tag.get_text(),
                    "link": link_tag["href"],
                    "snippet": snippet_tag.get_text() if snippet_tag else ""
                })
        return results
    except Exception as e:
        print("Błąd scrapowania:", e)
        return []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q","")
    offset = int(request.args.get("offset",0))
    if not query:
        return jsonify([])
    results = scrape_duckduckgo(query)
    return jsonify(results[offset:offset+10])

if __name__ == "__main__":
    app.run(debug=True)










