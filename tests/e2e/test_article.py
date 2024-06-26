import re
import os
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright
from portmap.core.models import Article, Feedback
from tests.core.fixtures.factories import ArticleFactory

# Tests for articles

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
        article = ArticleFactory()
        page = self.context.new_page()
        page.goto('/articles/' + article.name + '/')
        expect(page.locator('form#query_form textarea[name=explanation]')).to_be_hidden()

    def test_happy_reaction(self):
        article = ArticleFactory()
        page = self.context.new_page()
        page.goto('/articles/' + article.name + '/')
        page.locator('form#query_form input[value=happy]').click()
        page.get_by_text('Give feedback').click();
        expect(page).to_have_url('/articles/' + article.name + '/feedback')
        feedbackCollection = Feedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.article.name == article.name
        assert newFeedback.reaction == 'happy'

    def test_sad_reaction(self):
        article = ArticleFactory()
        page = self.context.new_page()
        page.goto('/articles/' + article.name + '/')
        page.locator('form#query_form input[value=sad]').click()
        page.get_by_text('Give feedback').click();
        expect(page).to_have_url('/articles/' + article.name + '/feedback')
        feedbackCollection = Feedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.article.name == article.name
        assert newFeedback.reaction == 'sad'

    def test_reaction_explanation(self):
        mock_explanation = 'TEST FEEDBACK FROM PLAYWRIGHT'
        article = ArticleFactory()
        page = self.context.new_page()
        page.goto('/articles/' + article.name + '/')
        page.locator('form#query_form input[value=happy]').click()
        page.locator('form#query_form textarea[name=explanation]').fill(mock_explanation)
        page.get_by_text('Give feedback').click();
        expect(page).to_have_url('/articles/' + article.name + '/feedback')
        feedbackCollection = Feedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.article.name == article.name
        assert newFeedback.explanation == mock_explanation

