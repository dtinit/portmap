import os
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright
from portmap.core.models import UseCaseFeedback, Article
from tests.core.fixtures.factories import ArticleFactory

# Tests for the find_articles query

class FindArticlesTests(StaticLiveServerTestCase):
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

    # When there are multiple matching articles,
    # the user is presented a list to choose from and a feedback form.
    @pytest.mark.django_db
    def test_usecase_feedback_form(self):
        mock_explanation = 'TEST FEEDBACK FROM PLAYWRIGHT'
        article1 = ArticleFactory()
        article2 = ArticleFactory(
            datatype=article1.datatype,
            sources=article1.sources,
            destinations=article1.destinations
        )

        page = self.context.new_page()
        page.goto('/find_articles?datatype=' + article1.datatype
                  + '&datasource=' + article1.sources
                  + '&datadest=' + article1.destinations)

        page.locator('form#multiple_option_feedback_form textarea').fill(mock_explanation)
        page.get_by_text('Give Feedback').click()
        expect(page).to_have_url('/usecase_feedback')
        feedbackCollection = UseCaseFeedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.explanation == mock_explanation
        assert newFeedback.datatype == article1.datatype
        assert newFeedback.source == article1.sources
        assert newFeedback.destination == article1.destinations

