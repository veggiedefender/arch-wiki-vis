import os
from bs4 import BeautifulSoup
import networkx as nx

G = nx.Graph()

BASE_DIR = "/usr/share/doc/arch-wiki/html/en/"
files = []
for root, dirs, names in os.walk(BASE_DIR):
    for name in names:
        files.append(os.path.join(root, name))

def remove_articles(files):
    return [file for file in files if ":" not in file]

def to_title(url):
    url = url.split("/")[-1]
    url = url.split("#")[0][:-5]
    return url

for filename in remove_articles(files):
    path = os.path.join(BASE_DIR, filename)
    with open(path) as f:
        title = to_title(filename)
        G.add_node(title)

        soup = BeautifulSoup(f, 'html.parser')
        body = soup.find(id="mw-content-text")
        links = [link.get("href") for link in body.find_all('a')]
        for link in remove_articles(links):
            if link.startswith(".."):
                link = to_title(link)
                G.add_edge(title, link)

nx.write_gexf(G, "graph.gexf")
