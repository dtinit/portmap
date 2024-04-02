import re
from playwright.sync_api import Page, Route, expect

# Smoke tests to make sure the site's primary functions are working

def test_has_title(page: Page):
    page.goto("http://localhost:8000")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("PortMap"))

def test_query(page: Page):
    page.goto("http://localhost:8000")

    page.get_by_text('Contacts').click()
    page.get_by_label('Transfer from').select_option('iCloud')
    page.get_by_text('Find Article').click()

    # This will break if the filename changes or another matching article is added
    expect(page).to_have_url('http://localhost:8000/articles/contacts1.md/')
