from playwright.sync_api import Page, Locator

from core.pages.base_page import BasePage


class BaseComponent(BasePage):
    def __init__(self, unique_locator: str, locators, owner: BasePage):
        super().__init__(
            page=owner.page,
            unique_locator=unique_locator,
            locators=locators,
        )
        self.owner = owner
