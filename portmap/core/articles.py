import base64
import requests

REPOSITORY_URL = "https://api.github.com/repos/dtinit/portability-articles"

def get_content_files():

    articles_list = requests.get(f"{REPOSITORY_URL}/contents/articles")

def get_article(name):
    article = requests.get(f"{REPOSITORY_URL}/contents/articles/{name}")
    article_data = article.json()
    return base64.b64decode(bytearray(article_data["content"], "utf-8"))
