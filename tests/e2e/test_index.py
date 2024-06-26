import re
import os
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright
from portmap.core.articles import get_content_files
from portmap.core.models import UseCaseFeedback, Article, DataType

# Tests for the root index page

class IndexTests(StaticLiveServerTestCase):
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

    def test_has_title(self):
        page = self.context.new_page()
        page.goto("/")
        expect(page).to_have_title("PortMap")

    # Loop through all the datatypes, sources, and destinations to validate them
    def test_datatypes_and_articles(self):
        get_content_files()
        page = self.context.new_page()
        page.goto("/")

        datatypes = page.locator('label.radiogrid').all()
        assert len(datatypes) > 0
        source_dropdown = page.get_by_label('Transfer from')
        destination_dropdown = page.get_by_label(' to', exact=True)

        def validate_current_source():
            destinations = destination_dropdown.get_by_role('option').all()
            destination_count = len(destinations)
            assert destination_count > 1 # One option is a placeholder
            # Loop through every destination
            for destination_index in range(1, destination_count):
                destination_dropdown.select_option(index=destination_index)
                with page.expect_response(re.compile("/find_articles(?:\?.*)?")) as response_info:
                    page.get_by_text('Find Article').click()
                query_response = response_info.value
                # When there's only one article, we redirect to it
                if query_response.status == 302:
                    expect(page).to_have_url(re.compile("/articles/.*\.md/"))
                    expect(page.locator('.page')).to_have_count(1)
                # Otherwise, we return a list of matching articles
                else:
                    assert query_response.ok
                    expect(page.locator('td > a')).not_to_have_count(0)

                page.go_back()

        def validate_datatype(datatype):
            datatype.click()
            expect(source_dropdown).to_be_enabled()
            # The destination dropdown is disabled until a source is selected
            expect(page.get_by_label(' to', exact=True)).to_be_disabled()
            sources = source_dropdown.get_by_role('option').all()
            source_count = len(sources)
            assert source_count > 1 # One option is a placeholder
            # Loop through every source
            for source_index in range(1, source_count):
                source_dropdown.select_option(index=source_index)
                validate_current_source()

        # The source dropdown is disabled until a datatype is selected
        expect(source_dropdown).to_be_disabled()
        for datatype in datatypes:
            validate_datatype(datatype)

    @pytest.mark.django_db
    def test_usecase_feedback_form(self):
        mock_explanation = 'TEST FEEDBACK FROM PLAYWRIGHT'
        page = self.context.new_page()
        page.goto('/')
        page.get_by_text("Can't see the option you're looking for?").click()
        page.locator('form#multiple_option_feedback_form textarea').fill(mock_explanation)
        page.get_by_text('Give Feedback').click()
        expect(page).to_have_url('/usecase_feedback')
        feedbackCollection = UseCaseFeedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.explanation == mock_explanation

