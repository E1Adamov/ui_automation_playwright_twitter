from playwright.sync_api import Page, Locator

from core.pages.base_page import BasePage
from core.locators.base_locators import BaseLocators


class EnterPasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(
            page=page,
            unique_locator='//span[text()="Enter your password"]',
            locators=EnterPasswordPageLocators(scope=page),
        )


class EnterPasswordPageLocators(BaseLocators):
    def input_password(self) -> Locator:
        return self.scope.locator("input[type=password]")

    def button_log_in(self) -> Locator:
        return self.scope.locator("div[role=button]", has_text="Log in")
