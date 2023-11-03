import base64
import requests
from portmap.utils import has_yaml_header

REPOSITORY_URL = "https://api.github.com/repos/dtinit/portability-articles"

def get_content_files():

    articles_response = requests.get(f"{REPOSITORY_URL}/contents/articles")
    debug_articles_info = []
    for article_item in articles_response.json():
        article_content = get_article(article_item['name'])
        article_header = "None"
        if has_yaml_header(str(article_content)):
            article_header = False
        debug_articles_info.append({"Article": article_item['name'], "Header": article_header})

    return debug_articles_info

def get_article(name):
    article = requests.get(f"{REPOSITORY_URL}/contents/articles/{name}")
    article_data = article.json()
    return base64.b64decode(bytearray(article_data["content"], "utf-8"))
