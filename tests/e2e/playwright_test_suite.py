import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

# Sets up playwright and ensures tests don't throw client-side errors
class PlaywrightTestSuite(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            headless=True # Change to False to observe tests running in Chromium locally
        )
        cls.context = cls.browser.new_context(base_url=cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    # Define a new page object for each test and listen for errors
    def setUp(self):
        self.page = self.context.new_page()
        self.page_errors = [];
        self.page.on("pageerror", lambda exception: self.page_errors.append(exception))
        self.console_errors = [];
        self.page.on("console", lambda msg: self.console_errors.append(f"{msg.text}") if msg.type == "error" else None)

    # Assert no uncaught errors were thrown, otherwise report them to the console
    def tearDown(self):
        self.page.close()
        assert len(self.page_errors) == 0, f"Uncaught page errors: {self.page_errors}"
        assert len(self.console_errors) == 0, f"Uncaught JS console errors: {self.console_errors}"

