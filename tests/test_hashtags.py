import logging
from typing import DefaultDict
from collections import defaultdict

import pytest

from core.components.tweet_component import Tweet
from core.pages.home_page import HomePage

logger = logging.getLogger(__name__)


@pytest.mark.get_tweets(author="google", count=100)
def test_google_hash_tags(home_page: HomePage, tweets: list[Tweet]):
    total_hash_tags_count = 0
    each_hash_tag_count: DefaultDict[str, int] = defaultdict(int)
    for tweet in tweets:
        for hash_tag in tweet.hash_tags:
            total_hash_tags_count += 1
            each_hash_tag_count[hash_tag] += 1

    logger.info(f"Total hash tags in 100 tweets: {total_hash_tags_count}")
    logger.info(f"Each hash tag count: {dict(each_hash_tag_count)}")