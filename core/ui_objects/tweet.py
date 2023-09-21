import re

from playwright.sync_api import Locator
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from core.locators.base_locators import BaseLocators
from core.pages.base_page import BasePage
from core.ui_objects.base_ui_object import BaseUiObject


class TweetLocators(BaseLocators):
    def text(self) -> Locator:
        return self.scope.locator("[data-testid=tweetText]")

    def mention(self) -> Locator:
        return self.text().locator("a[role=link]", has_text=re.compile(r"^@.*"))

    def hash_tag(self) -> Locator:
        return self.scope.locator(
            "a[role=link][href^='/hashtag/']", has_text=re.compile(r"^#.*")
        )


class Tweet(BaseUiObject):
    def __init__(self, owner: BasePage, locator: Locator):
        super().__init__(
            unique_locator="div[data-testid='tweetText']",
            locators=TweetLocators(scope=locator),
            owner=owner,
            locator=locator,
        )
        self.mentions: list[str] = self.get_mentions()
        self.hash_tags: list[str] = self.get_hash_tags()

    def get_mentions(self) -> list[str]:
        return self._get_internal_elements(locator=self.locators.mention())

    def get_hash_tags(self) -> list[str]:
        return self._get_internal_elements(locator=self.locators.hash_tag())

    @staticmethod
    def _get_internal_elements(locator: Locator):
        try:
            locator.last.wait_for(timeout=500)
        except PlaywrightTimeoutError:
            elements = []
        else:
            elements = locator.all_text_contents()
        return elements
