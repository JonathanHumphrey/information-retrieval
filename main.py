import csv
import requests
import os

import codecs

from dotenv import load_dotenv, find_dotenv
# whoosh imports
from whoosh import index
from whoosh.writing import BufferedWriter
from whoosh.fields import Schema, ID, NUMERIC, TEXT
from whoosh.qparser import QueryParser
from whoosh.index import create_in
# Flask imports
from flask import Flask, render_template, request

# App instantiation
app = Flask(__name__)
schema = Schema(year=NUMERIC(stored=True),
                rank=NUMERIC(stored=True),
                title=TEXT(stored=True),
                artist=TEXT(stored=True),
                lyrics=TEXT(stored=True),
                snippet=TEXT(stored=True))

# ROUTING
@app.route('/')
def landing_page():
    return render_template("landingPage.html")
@app.route('/local-search', methods=['POST', 'GET'])
def local_search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        
        ix = index.open_dir("index")
        with ix.searcher() as searcher:
            parser = QueryParser("lyrics", schema=ix.schema)
            q = parser.parse(keyword)
            results = []
            for hit in searcher.search(q, limit=None):
                snippet = hit.highlights("lyrics")
                if not snippet:
                    snippet = hit['lyrics'][:100] + "..."
                result = {
                    'title': hit['title'],
                    'artist': hit['artist'],
                    'year': hit['year'],
                    'rank': hit['rank'],
                    'snippet': snippet
                }
                results.append(result)
            return render_template("localResults.html",query=keyword, results=results)
    else:
        return render_template("localSearch.html")

@app.route('/web-search', methods=['POST', 'GET'])
def web_search():
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        results = bing_search(query)
        return render_template("webResults.html", results=results)
    else: 
        return render_template("webSearch.html")



# PROCESSING
@app.route("/details/<data>")
def details(data):
    return render_template("details.html", data=data)


# @desc: Forms the dictionary of all music based on year
def setup():
    index_dir = "index"
    index = create_in(index_dir, schema)

    with index.writer() as writer:
        with open("output.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                writer.add_document(year=int(row["Year"]),
                                    rank=int(row["Rank"]),
                                    title=row["Song"],
                                    artist=row["Artist"],
                                    lyrics=row["Lyrics"]) 



def bing_search(query):
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("API_KEY")
    }
    params = {
        "q": query,
        "textDecorations": True,
        "textFormat": "HTML",
        "count" : 10
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()['webPages']['value']

data = setup()

