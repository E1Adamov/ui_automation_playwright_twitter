from playwright.sync_api import Page

from core.components.tweet_component import TweetComponent
from core.locators.base_locators import BaseLocators
from core.pages.base_page import BasePage


class AuthorTweetsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(
            page=page,
            unique_locator='div[aria-label="Timeline: Your Home Timeline"]',
            locators=AuthorTweetsPageLocators(scope=page),
        )
        self.tweet_component = TweetComponent(owner=self)


class AuthorTweetsPageLocators(BaseLocators):
    ...
