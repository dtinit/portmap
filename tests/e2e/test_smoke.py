import re
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright
from portmap.core.articles import get_content_files

# Smoke tests to make sure the site's primary functions are working

class SmokeTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_has_title(self):
        page = self.browser.new_page()
        page.goto(self.live_server_url)
        expect(page).to_have_title(re.compile("PortMap"))

    def test_query(self):
        get_content_files()
        page = self.browser.new_page()
        page.goto(self.live_server_url)
        page.get_by_text('Contacts').click()
        page.get_by_label('Transfer from').select_option('iCloud')
        page.get_by_text('Find Article').click()
        # This will break if the filename changes or another matching article is added
        expect(page).to_have_url(f"{self.live_server_url}/articles/contacts1.md/")
