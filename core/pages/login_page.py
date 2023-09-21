from playwright.sync_api import Page, Locator

from core.pages.base_page import BasePage
from core.locators.base_locators import BaseLocators


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(
            page=page,
            unique_locator='//span[]text()="Sign in to X"',
            locators=LoginPageLocators(scope=page),
        )


class LoginPageLocators(BaseLocators):
    def input_user_name(self) -> Locator:
        return self.scope.locator("input[autocomplete=username]")

    def button_next(self) -> Locator:
        return self.scope.locator("div[role=button]", has_text="Next")
