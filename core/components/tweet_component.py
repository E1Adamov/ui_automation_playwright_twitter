import logging
import time
from typing import Optional

from playwright.sync_api import Locator, ElementHandle

from core.components.base_component import BaseComponent
from core.locators.base_locators import BaseLocators
from core.ui_objects.tweet import Tweet


logger = logging.getLogger(__name__)


class TweetComponentLocators(BaseLocators):
    def article(self) -> Locator:
        return self.scope.locator("article[data-testid=tweet]")


class TweetComponent(BaseComponent):
    def __init__(self, owner):
        super().__init__(
            owner=owner,
            unique_locator="article[data-testid=tweet]",
            locators=TweetComponentLocators(scope=owner.page),
        )

    def get_tweets(self, count: Optional[int] = None, timeout: int = 10) -> list[Tweet]:
        article_locator: Locator = self.locators.article()
        article_locator.last.wait_for()
        article_locators: list[Locator] = article_locator.all()
        tweets_batch: list[Tweet] = [
            Tweet(owner=self.owner, locator=article) for article in article_locators
        ]
        if count is None:
            return tweets_batch
        elif count <= len(tweets_batch):
            return tweets_batch[:count]
        else:
            tweets: dict[str, Tweet] = {
                tweet.locator.get_attribute("aria-labelledby"): tweet
                for tweet in tweets_batch
            }
            start = time.time()
            while len(tweets) < count and time.time() - start < timeout:
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 5)")
                article_locator.last.wait_for()
                article_locators: list[Locator] = article_locator.all()
                tweets_batch: list[Tweet] = [
                    Tweet(owner=self.owner, locator=article)
                    for article in article_locators
                ]
                tweets.update(
                    {
                        tweet.locator.get_attribute("aria-labelledby"): tweet
                        for tweet in tweets_batch
                    }
                )

            if len(tweets) < count:
                logger.warning(
                    f"Found only {len(tweets)} tweets after {time.time() - start} seconds"
                )

            return list(tweets.values())[:count]
