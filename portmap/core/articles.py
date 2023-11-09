import base64
import requests
from portmap.utils import extract_yaml_and_body
from django.conf import settings

REPOSITORY_URL = "https://api.github.com/repos/dtinit/portability-articles"

def get_content_files():
    auth = (settings.GITHUB_APP_ACCOUNT_ID, settings.GITHUB_APP_ACCOUNT_SECRET)
    articles_response = requests.get(f"{REPOSITORY_URL}/contents/articles", auth=auth)
    if articles_response.status_code != 200:
        raise Exception(f"Github API responded {articles_response.status_code}, {articles_response.content}")
    debug_articles_info = []
    for article_item in articles_response.json():
        article_content = get_article(article_item['name'])
        yaml_header, body = extract_yaml_and_body(article_content)
        article_dict = {**yaml_header,  "Article": article_item['name'],  "Body": body}
        debug_articles_info.append(article_dict)

    return debug_articles_info

def get_article(name):
    article = requests.get(f"{REPOSITORY_URL}/contents/articles/{name}", auth=(USER, PASSWORD))
    article_data = article.json()
    return base64.b64decode(bytearray(article_data["content"], "utf-8")).decode('utf-8')

def get_article_fields_table():
    debug_articles_info = get_content_files()
    for item in debug_articles_info:
        pass
