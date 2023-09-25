from playwright.sync_api import Page, Locator

from core.pages.base_page import BasePage
from core.locators.base_locators import BaseLocators


class ConfirmationCodePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(
            page=page,
            unique_locator='//*[text()="Check your email"]',
            locators=ConfirmationCodePageLocators(scope=page),
        )


class ConfirmationCodePageLocators(BaseLocators):
    def input_confirmation_code(self) -> Locator:
        return self.scope.locator("input")

    def button_next(self) -> Locator:
        return self.scope.locator("[role=button]", has_text="Next")
