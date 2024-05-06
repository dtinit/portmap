import os
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright
from portmap.core.models import UseCaseFeedback, Article

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
        mock_datatype = 'Mock Datatype'
        mock_source = 'Mock Source'
        mock_destination = 'Mock Destination'
        mock_explanation = 'TEST FEEDBACK FROM PLAYWRIGHT'

        Article.objects.create(
            name='article1',
            datatype=mock_datatype,
            sources=mock_source,
            destinations=mock_destination,
            title='Test article 1',
            body='Test article 1'
        )
        Article.objects.create(
            name='article2',
            datatype=mock_datatype,
            sources=mock_source,
            destinations=mock_destination,
            title='Test article 2',
            body='Test article 2'
        )

        page = self.context.new_page()
        page.goto('/find_articles?datatype=' + mock_datatype
                  + '&datasource=' + mock_source
                  + '&datadest=' + mock_destination)

        page.locator('form#multiple_option_feedback_form textarea').fill(mock_explanation)
        page.get_by_text('Give Feedback').click()
        expect(page).to_have_url('/usecase_feedback')
        feedbackCollection = UseCaseFeedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.explanation == mock_explanation
        assert newFeedback.datatype == mock_datatype
        assert newFeedback.source == mock_source
        assert newFeedback.destination == mock_destination

