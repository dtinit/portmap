import base64
import requests
from portmap.utils import extract_yaml_and_body
from django.conf import settings
from .models import Article
from portmap.github_auth import get_github_auth_token


def get_content_files():
    debug_articles_info = []
    gh = GithubClient()
    for article_item in gh.get_article_list():
        article_content = gh.get_article(article_item['name'])
        yaml_header, body = extract_yaml_and_body(article_content)
        article_dict = {**yaml_header, "Article": article_item['name'], "Body": body}
        debug_articles_info.append(article_dict)
        new_data = {'body': body,
                    'title': yaml_header['title'],
                    'datatype': yaml_header['datatype'],
                    'sources': yaml_header['sources'],
                    'destinations': yaml_header['destinations']}
        Article.objects.update_or_create(name=article_item['name'], defaults=new_data)

    return debug_articles_info

class GithubClient:
    REPOSITORY_URL = "https://api.github.com/repos/dtinit/portability-articles"

    def __init__(self):
        self.headers = {"Authorization": f"Bearer {get_github_auth_token()}"}

    def get_article_list(self):
        response = requests.get(f"{self.REPOSITORY_URL}/contents/articles", headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Github API responded {response.status_code}, {response.content} to {response.request.url}")

        return response.json()

    def get_article(self, name):
        article = requests.get(f"{self.REPOSITORY_URL}/contents/articles/{name}", headers=self.headers)
        article_data = article.json()
        return base64.b64decode(bytearray(article_data["content"], "utf-8")).decode('utf-8')

    def get_article_fields_table(self):
        debug_articles_info = self.get_article_list()
        for item in debug_articles_info:
            pass
