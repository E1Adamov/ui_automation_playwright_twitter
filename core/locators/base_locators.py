import abc

from playwright.sync_api import Page, Locator


class BaseLocators(abc.ABC):
    def __init__(self, scope: Page | Locator):
        self.scope = scope
