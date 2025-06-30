import pytest
from portmap.core.articles import process_article
from portmap.core.models import Article

pytestmark = pytest.mark.django_db


@pytest.fixture
def article_content():
    return """
---
title:  Download your watch history
datatype: "Viewing History"
sources: Fakestagram
destinations: ["Exampletok", "Sometube"]
---

# Download your watch history

Here are some instructions!

* An instruction
* Another bullet point
    """


def test_process_article(article_content):
    process_article('watch_history1.md', article_content)
    assert Article.objects.count() == 1


def test_process_bad_yaml(article_content):
    # Adding an extra comma at the end of the destinations list:
    article_content = article_content.replace('["Exampletok", "Sometube"]', '["Exampletok", "Sometube"],')
    with pytest.raises(RuntimeError) as err_info:
        process_article('watch_history1.md', article_content)
