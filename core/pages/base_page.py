from __future__ import annotations

import abc
from typing import Optional

from playwright.sync_api import Page


class BasePage(abc.ABC):
    def __init__(self, page: Page, unique_locator: str, locators):
        self.page: Page = page
        self.unique_locator = unique_locator
        self.locators = locators

    def __getattr__(self, item):
        return getattr(self.page, item)

    def wait_to_open(self, timeout: Optional[float] = None) -> BasePage:
        self.page.locator(self.unique_locator).wait_for(timeout=timeout)
        return self
