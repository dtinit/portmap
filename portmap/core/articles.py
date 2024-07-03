import base64
import requests
import yaml
import logging
import os
from django.conf import settings
from pathlib import Path
from portmap.utils import extract_yaml_and_body
from .models import Article, DataType
from portmap.github_auth import get_github_auth_token
from .views import render_index_to_string


def process_article(article_name, article_content):
    try:
        yaml_header, body = extract_yaml_and_body(article_content)
        new_data = {'body': body,
                    'title': yaml_header['title'],
                    'datatype': yaml_header['datatype'],
                    'sources': yaml_header['sources'],
                    'destinations': yaml_header['destinations']}
        Article.objects.update_or_create(name=article_name, defaults=new_data)

    except Exception as e:
        logging.error(f"Error processing article {article_name}: {e}")
        raise RuntimeError(f"Failed to process article '{article_name}'. Check for headers and datatype values.")


def get_content_files():
    gh = GithubClient()
    try:
        datatype_help = gh.get_datatype_help()
        for datatype_name in gh.get_datatype_help():
            helpText = datatype_help.get(datatype_name)
            DataType.objects.update_or_create(name=datatype_name, helpText=helpText)
        article_data = {}
        for article_item in gh.get_article_list():
            article_data[article_item['name']] = gh.get_article(article_item['name'])
    except Exception as e:
        logging.error(f"Error accessing Github API: {e}")
        raise RuntimeError("Failed to access Github API.")

    for article_name, article_body in article_data.items():
        process_article(article_name, article_body)

    # Generate a static copy of the root index.html
    try:
        # Make sure the directory exists since it's excluded from source control
        os.makedirs(settings.STATIC_VIEW_DIR, exist_ok=True)
        indexContent = render_index_to_string()
        with open(os.path.join(settings.STATIC_VIEW_DIR, "index.html"), "w") as indexFile:
            indexFile.write(indexContent)
    except Exception as e:
        logging.error(f"Error generating index file: {e}")
        raise RuntimeError("Failed to generate index file")


class GithubClient:
    REPOSITORY_URL = "https://api.github.com/repos/dtinit/portability-articles"

    def __init__(self):
        self.headers = {"Authorization": f"Bearer {get_github_auth_token()}"}

    def get_article_list(self):
        response = requests.get(f"{self.REPOSITORY_URL}/contents/articles", headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Github API responded {response.status_code}, {response.content} to {response.request.url}")

        return response.json()

    def get_github_file_content(self, filepath):
        article = requests.get(f"{self.REPOSITORY_URL}/contents/{filepath}", headers=self.headers)
        article_data = article.json()
        return base64.b64decode(bytearray(article_data["content"], "utf-8")).decode('utf-8')

    def get_article(self, name):
        return self.get_github_file_content(Path('articles') / name)

    def get_article_fields_table(self):
        debug_articles_info = self.get_article_list()
        for item in debug_articles_info:
            pass

    def get_datatype_help(self):
        raw_content = self.get_github_file_content('datatype-help.yaml')
        return yaml.safe_load(raw_content)
