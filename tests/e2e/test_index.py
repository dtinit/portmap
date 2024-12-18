import re
import pytest
from playwright.sync_api import expect
from portmap.core.articles import get_content_files
from portmap.core.models import UseCaseFeedback, Article, DataType
from .playwright_test_suite import PlaywrightTestSuite

# Tests for the root index page
class IndexTests(PlaywrightTestSuite):
    # Loop through all the datatypes, sources, and destinations to validate them
    def test_datatypes_and_articles(self):
        get_content_files()
        self.page.goto("/")

        datatypes = self.page.locator('label.radiogrid').all()
        assert len(datatypes) > 0
        source_dropdown = self.page.get_by_label('Transfer from')
        destination_dropdown = self.page.get_by_label(' to', exact=True)

        def validate_current_source():
            destinations = destination_dropdown.get_by_role('option').all()
            destination_count = len(destinations)
            assert destination_count > 1 # One option is a placeholder
            # Loop through every destination
            for destination_index in range(1, destination_count):
                destination_dropdown.select_option(index=destination_index)
                with self.page.expect_response(re.compile("/find_articles(?:\?.*)?")) as response_info:
                    self.page.get_by_text('Find Article').click()
                query_response = response_info.value
                # When there's only one article, we redirect to it
                if query_response.status == 302:
                    expect(self.page).to_have_url(re.compile("/articles/.*\.md/"))
                    expect(self.page.locator('.page')).to_have_count(1)
                # Otherwise, we return a list of matching articles
                else:
                    assert query_response.ok
                    expect(self.page.locator('td > a')).not_to_have_count(0)

                self.page.go_back()

        def validate_datatype(datatype):
            datatype.click()
            expect(source_dropdown).to_be_enabled()
            # The destination dropdown is disabled until a source is selected
            expect(self.page.get_by_label(' to', exact=True)).to_be_disabled()
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
        self.page.goto('/')
        self.page.get_by_text("Can't see the option you're looking for?").click()
        self.page.locator('form#multiple_option_feedback_form textarea').fill(mock_explanation)
        self.page.get_by_text('Give Feedback').click()
        expect(self.page).to_have_url('/usecase_feedback')
        feedbackCollection = UseCaseFeedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.explanation == mock_explanation

