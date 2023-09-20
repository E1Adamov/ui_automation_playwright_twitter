import logging
from typing import DefaultDict
from collections import defaultdict

import pytest

from core.components.tweet_component import Tweet
from core.pages.home_page import HomePage

logger = logging.getLogger(__name__)


@pytest.mark.get_tweets(author="google", count=100)
def test_google_mentions(home_page: HomePage, tweets: list[Tweet]):
    total_mentions_count = 0
    each_mention_count: DefaultDict[str, int] = defaultdict(int)
    for tweet in tweets:
        for mention in tweet.mentions:
            total_mentions_count += 1
            each_mention_count[mention] += 1

    logger.info(f"Total mentions in 100 tweets: {total_mentions_count}")
    logger.info(f"Each mention count: {dict(each_mention_count)}")
