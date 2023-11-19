import pytest
from playwright.sync_api import sync_playwright

from .core.fixtures.factories import *


@pytest.fixture()
def browser():
    with sync_playwright() as p:
        for browser_type in [p.firefox]:
            browser = browser_type.launch()
            yield browser
            browser.close()


@pytest.fixture()
def page(browser):
    return browser.new_page()
