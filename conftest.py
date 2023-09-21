import os
from urllib.parse import urljoin

import pytest
from _pytest.config.argparsing import Parser
from playwright.sync_api import Browser

from core.components.tweet_component import Tweet
from core.pages.author_tweet_page import AuthorTweetsPage
from core.pages.enter_password_page import EnterPasswordPage
from core.pages.home_page import HomePage
from core.pages.login_page import LoginPage
from root import ROOT_PATH


def pytest_addoption(parser: Parser):
    parser.addoption("--env", required=True, help="Base URL")
    parser.addoption(
        "--TWITTER_USER_NAME",
        required=True,
        help='Example: --TWITTER_USER_NAME="@myUserName"',
    )
    parser.addoption(
        "--TWITTER_PASSWORD",
        required=True,
        help='Example: --TWITTER_PASSWORD="mysecretpassword"',
    )
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

    home_page = HomePage(page=page)
    home_page.wait_to_open()

    state_storage_path = os.path.join(ROOT_PATH, "temp", "state.json")
    context.storage_state(path=state_storage_path)

    page.close()
    yield state_storage_path


@pytest.fixture(autouse=True)
def home_page(
    request: pytest.FixtureRequest,
    browser: Browser,
    login_and_save_state: str,
) -> HomePage:
    context = browser.new_context(storage_state=login_and_save_state)
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


@pytest.fixture()
def tweets(
    request: pytest.FixtureRequest,
    home_page: HomePage,
) -> list[Tweet]:
    marker = request.node.get_closest_marker("get_tweets")
    author = marker.kwargs["author"]
    count = marker.kwargs["count"]

    env_url = request.config.option.env
    author_page_url = urljoin(env_url, author)
    home_page.goto(author_page_url)

    author_tweet_page = AuthorTweetsPage(page=home_page.page)
    tweets: list[Tweet] = author_tweet_page.tweet_component.get_tweets(
        count=count, timeout=120
    )

    return tweets
