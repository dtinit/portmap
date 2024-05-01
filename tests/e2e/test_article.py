import re
import os
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright
from portmap.core.models import Article

# Tests for articles

def create_test_article():
    Article.objects.create(
        name='testarticle.md',
        datatype="DT",
        sources='Test source',
        destinations='Test destination',
        title='Test article',
        body='This article is just a test.')

class ArticleTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.context = cls.browser.new_context(base_url=cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_reaction_form_requires_selection(self):
        create_test_article()
        page = self.context.new_page()
        page.goto("/articles/testarticle.md/")
        expect(page.locator('form#query_form textarea[name=explanation]')).to_be_hidden()

    def test_happy_reaction(self):
        create_test_article()
        page = self.context.new_page()
        page.goto("/articles/testarticle.md/")
        page.locator('form#query_form input[value=happy]').click()
        with page.expect_request('/articles/testarticle.md/feedback') as request_info:
            page.get_by_text('Give feedback').click();

        expect(page).to_have_url('/articles/testarticle.md/feedback')
        assert request_info.value.post_data_json['reaction'] == 'happy'

    def test_sad_reaction(self):
        create_test_article()
        page = self.context.new_page()
        page.goto("/articles/testarticle.md/")
        page.locator('form#query_form input[value=sad]').click()
        with page.expect_request('/articles/testarticle.md/feedback') as request_info:
            page.get_by_text('Give feedback').click();

        expect(page).to_have_url('/articles/testarticle.md/feedback')
        assert request_info.value.post_data_json['reaction'] == 'sad'

    def test_reaction_explanation(self):
        create_test_article()
        page = self.context.new_page()
        page.goto("/articles/testarticle.md/")
        page.locator('form#query_form input[value=happy]').click()
        page.locator('form#query_form textarea[name=explanation]').fill('TEST FEEDBACK FROM PLAYWRIGHT')
        with page.expect_request('/articles/testarticle.md/feedback') as request_info:
            page.get_by_text('Give feedback').click();

        expect(page).to_have_url('/articles/testarticle.md/feedback')
        assert request_info.value.post_data_json['explanation'] == 'TEST FEEDBACK FROM PLAYWRIGHT'

