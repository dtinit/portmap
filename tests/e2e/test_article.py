from playwright.sync_api import expect
from portmap.core.models import Article, Feedback
from tests.core.fixtures.factories import ArticleFactory
from .playwright_test_suite import PlaywrightTestSuite

# Tests for articles

class ArticleTests(PlaywrightTestSuite):
    def test_reaction_form_requires_selection(self):
        article = ArticleFactory()
        self.page.goto('/articles/' + article.name + '/')
        expect(self.page.locator('form#query_form textarea[name=explanation]')).to_be_hidden()

    def test_happy_reaction(self):
        article = ArticleFactory()
        self.page.goto('/articles/' + article.name + '/')
        self.page.locator('form#query_form input[value=happy]').click()
        self.page.get_by_text('Give feedback').click();
        expect(self.page).to_have_url('/articles/' + article.name + '/feedback')
        feedbackCollection = Feedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.article.name == article.name
        assert newFeedback.reaction == 'happy'

    def test_sad_reaction(self):
        article = ArticleFactory()
        self.page.goto('/articles/' + article.name + '/')
        self.page.locator('form#query_form input[value=sad]').click()
        self.page.get_by_text('Give feedback').click();
        expect(self.page).to_have_url('/articles/' + article.name + '/feedback')
        feedbackCollection = Feedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.article.name == article.name
        assert newFeedback.reaction == 'sad'

    def test_reaction_explanation(self):
        mock_explanation = 'TEST FEEDBACK FROM PLAYWRIGHT'
        article = ArticleFactory()
        self.page.goto('/articles/' + article.name + '/')
        self.page.locator('form#query_form input[value=happy]').click()
        self.page.locator('form#query_form textarea[name=explanation]').fill(mock_explanation)
        self.page.get_by_text('Give feedback').click();
        expect(self.page).to_have_url('/articles/' + article.name + '/feedback')
        feedbackCollection = Feedback.objects.all()
        assert len(feedbackCollection) == 1
        newFeedback = feedbackCollection.first()
        assert newFeedback.article.name == article.name
        assert newFeedback.explanation == mock_explanation

