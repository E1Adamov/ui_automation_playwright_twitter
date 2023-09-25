import logging
import os
import time
from urllib.parse import urljoin

import pytest
from _pytest.config.argparsing import Parser
from playwright.sync_api import Browser
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

from core.components.tweet_component import Tweet
from core.pages.author_tweet_page import AuthorTweetsPage
from core.pages.confirmation_code_page import ConfirmationCodePage
from core.pages.enter_password_page import EnterPasswordPage
from core.pages.home_page import HomePage
from core.pages.login_page import LoginPage
from root import ROOT_PATH
from core.helpers import gmail


tweets_cache = {}


def pytest_addoption(parser: Parser):
    parser.addoption("--env", required=True, help="Base URL")
    parser.addoption("--TWITTER_USER_NAME", required=True)
    parser.addoption("--TWITTER_PASSWORD", required=True)
    parser.addoption("--GMAIL_USER_NAME")
    parser.addoption("--GMAIL_PASSWORD")
    parser.addoption("--screen_width", required=True, type=int)
    parser.addoption("--screen_height", required=True, type=int)


@pytest.fixture(scope="session")
def login_and_save_state(request: pytest.FixtureRequest, browser: Browser) -> str:
    user_name = request.config.option.TWITTER_USER_NAME
    password = request.config.option.TWITTER_PASSWORD
    env_url = request.config.option.env

    context = browser.new_context()
    page = context.new_page()
    url = urljoin(env_url, "i/flow/login")
    page.goto(url=url)

    login_page = LoginPage(page=page)
    login_page.locators.input_user_name().fill(user_name)
    login_page.locators.button_next().click()

    enter_password_page = EnterPasswordPage(page=page)
    enter_password_page.locators.input_password().fill(password)
    enter_password_page.locators.button_log_in().click()

    confirmation_code_page = ConfirmationCodePage(page=page)
    try:
        confirmation_code_page.wait_to_open(timeout=10000)
    except PlaywrightTimeoutError:
        pass
    else:
        gmail_user_name = request.config.option.GMAIL_USER_NAME
        gmail_password = request.config.option.GMAIL_PASSWORD
        confirmation_code = gmail.get_confirmation_code(
            email=gmail_user_name, password=gmail_password
        )
        confirmation_code_page.locators.input_confirmation_code().fill(
            confirmation_code
        )
        confirmation_code_page.locators.button_next().click()

    home_page = HomePage(page=page)
    home_page.wait_to_open()

    state_storage_path = os.path.join(ROOT_PATH, "temp", "state.json")
    context.storage_state(path=state_storage_path)

    page.close()
    yield state_storage_path


@pytest.fixture
def home_page(
    request: pytest.FixtureRequest,
    browser: Browser,
    login_and_save_state: str,
) -> HomePage:
    context = browser.new_context(
        storage_state=login_and_save_state,
        record_video_dir=os.path.join(ROOT_PATH, "reports"),
    )
    page = context.new_page()

    width = request.config.option.screen_width
    height = request.config.option.screen_height
    page.set_viewport_size({"width": width, "height": height})

    env_url = request.config.option.env
    page.goto(env_url)
    home_page = HomePage(page=page)
    home_page.wait_to_open()
    yield home_page

    page.close()


@pytest.fixture
def cacheable_tweets(
    request: pytest.FixtureRequest,
    home_page: HomePage,
) -> list[Tweet]:
    marker = request.node.get_closest_marker("get_tweets")
    author = marker.kwargs["author"]
    count = marker.kwargs["count"]

    cache_key = (author, count)
    if cache_key in tweets_cache:
        return tweets_cache[cache_key]

    env_url = request.config.option.env
    author_page_url = urljoin(env_url, author)
    home_page.goto(author_page_url)

    author_tweet_page = AuthorTweetsPage(page=home_page.page)
    tweets: list[Tweet] = author_tweet_page.tweet_component.get_tweets(
        count=count, timeout=120
    )

    tweets_cache[cache_key] = tweets

    return tweets
