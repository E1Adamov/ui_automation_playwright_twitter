from playwright.sync_api import Locator

from core.components.base_component import BaseComponent
from core.pages.base_page import BasePage


class BaseUiObject(BaseComponent):
    def __init__(
        self, unique_locator: str, locators, owner: BasePage, locator: Locator
    ):
        super().__init__(
            unique_locator=unique_locator,
            locators=locators,
            owner=owner,
        )
        self.locator: Locator = locator

    def __getattr__(self, item):
        return getattr(self.locator, item)
