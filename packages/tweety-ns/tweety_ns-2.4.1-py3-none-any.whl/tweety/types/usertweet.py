import traceback

from .twDataTypes import SelfThread, ConversationThread, Tweet, Excel, ScheduledTweet
from ..exceptions import UserProtected, UserNotFound
from .base import BaseGeneratorClass, find_objects
from ..filters import TweetCommentFilters


class UserTweets(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }
    _RESULT_ATTR = "tweets"

    def __init__(self, user_id, client, pages=1, get_replies: bool = True, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.get_replies = get_replies
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time
        self.pinned = None

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def _get_pinned_tweet(self, response):
        pinned = find_objects(response, "type", "TimelinePinEntry", recursive=False, none_value={})
        pinned_tweet = Tweet(self.client, pinned, None)
        return pinned_tweet

    async def get_page(self, cursor):
        _tweets = []

        response = await self.client.http.get_tweets(self.user_id, replies=self.get_replies, cursor=cursor)

        if not response['data']['user'].get("result"):
            raise UserNotFound(response=response)

        if response['data']['user']['result']['__typename'] == "UserUnavailable":
            raise UserProtected(403, "UserUnavailable", response)

        entries = self._get_entries(response)

        if not self.pinned:
            self.pinned = self._get_pinned_tweet(response)

        for entry in entries:
            object_type = self._get_target_object(entry)

            try:
                if object_type is None:
                    continue

                parsed = object_type(self.client, entry, None)
                if parsed:
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top

    def to_xlsx(self, filename=None):
        return Excel(self, filename)


class UserHighlights(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }
    _RESULT_ATTR = "tweets"

    def __init__(self, user_id, client, pages=1, get_replies: bool = True, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.get_replies = get_replies
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time
        self.pinned = None

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    async def get_page(self, cursor):
        _tweets = []

        response = await self.client.http.get_highlights(self.user_id, cursor=cursor)

        if not response['data']['user'].get("result"):
            raise UserNotFound(response=response)

        if response['data']['user']['result']['__typename'] == "UserUnavailable":
            raise UserProtected(403, "UserUnavailable", response)

        entries = self._get_entries(response)

        for entry in entries:
            object_type = self._get_target_object(entry)

            try:
                if object_type is None:
                    continue

                parsed = object_type(self.client, entry, None)
                if parsed:
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top

    def to_xlsx(self, filename=None):
        return Excel(self, filename)


class UserLikes(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }
    _RESULT_ATTR = "tweets"

    def __init__(self, user_id, client, pages=1, get_replies: bool = True, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.get_replies = get_replies
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time
        self.pinned = None

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    async def get_page(self, cursor):
        _tweets = []

        response = await self.client.http.get_likes(self.user_id, cursor=cursor)

        if not response['data']['user'].get("result"):
            raise UserNotFound(response=response)

        if response['data']['user']['result']['__typename'] == "UserUnavailable":
            raise UserProtected(403, "UserUnavailable", response)

        entries = self._get_entries(response)

        for entry in entries:
            object_type = self._get_target_object(entry)

            try:
                if object_type is None:
                    continue

                parsed = object_type(self.client, entry, None)
                if parsed:
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top

    def to_xlsx(self, filename=None):
        return Excel(self, filename)


class UserMedia(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": Tweet
    }
    _RESULT_ATTR = "tweets"

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    @staticmethod
    def _result_attr():
        return "tweets"

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    async def get_page(self, cursor):
        _tweets = []

        response = await self.client.http.get_medias(self.user_id, cursor=cursor)
        if not response['data']['user'].get("result"):
            raise UserNotFound(response=response)

        if response['data']['user']['result']['__typename'] == "UserUnavailable":
            raise UserProtected(403, "UserUnavailable", response)

        entries = find_objects(response, "tweetDisplayType", "MediaGrid", none_value=[])

        for entry in entries:
            object_type = Tweet

            try:
                if object_type is None:
                    continue

                parsed = object_type(self.client, entry, None)
                if parsed:
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top


class SelfTimeline(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }
    _RESULT_ATTR = "tweets"

    def __init__(self, user_id, client, timeline_type, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.is_next_page = True
        self.timeline_type = timeline_type
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    async def get_page(self, cursor):
        _tweets = []
        response = await self.client.http.get_home_timeline(timeline_type=self.timeline_type,cursor=cursor)

        entries = self._get_entries(response)

        for entry in entries:
            object_type = self._get_target_object(entry)

            try:
                if object_type is None:
                    continue

                parsed = object_type(self.client, entry, None)
                if parsed:
                    _tweets.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top


class TweetComments(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "conversationthread": ConversationThread,
        "tweet": Tweet,
    }
    _RESULT_ATTR = "tweets"

    def __init__(self, tweet_id, client, get_hidden=False, filter_=TweetCommentFilters.Relevant, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.is_next_page = True
        self.get_hidden = get_hidden
        self.client = client
        self.tweet_id = tweet_id
        self.pages = pages
        self.filter= filter_
        self.wait_time = wait_time
        self.parent = None
        self.ignore_empty_list = False

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    async def _get_parent(self):
        return self.tweet_id if isinstance(self.tweet_id, Tweet) else await self.client.tweet_detail(self.tweet_id)

    async def get_page(self, cursor):
        _comments = []
        if not self.parent:
            self.parent = await self._get_parent()
        if self.get_hidden:
            response = await self.client.http.get_hidden_comments(self.tweet_id, cursor)
        else:
            response = await self.client.http.get_tweet_detail(self.tweet_id, cursor, self.filter)

        entries = self._get_entries(response)

        for entry in entries:
            object_type = self._get_target_object(entry)

            try:
                if object_type is None:
                    continue
                if "Tweet" in str(object_type):
                    entry = [entry]
                    object_type = ConversationThread
                else:
                    entry = [i for i in entry.get('content', {}).get('items', [])]


                if len(entry) > 0:
                    parsed = object_type(self.client, self.parent, entry)
                    _comments.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")
        cursor_spam = self._get_cursor_(response, "ShowMoreThreadsPrompt") or self._get_cursor_(response, "ShowMoreThreads")
        if cursor_spam:
            cursor = cursor_spam

        return _comments, cursor, cursor_top

    def __repr__(self):
        return "TweetComments(tweet_id={}, count={}, filter={}, parent={})".format(
            self.tweet_id, len(self.tweets), self.filter, self.parent
        )


class TweetHistory(BaseGeneratorClass):
    LATEST_TWEET_ENTRY_ID = "latestTweet"

    def __init__(self, tweet_id, client):
        super().__init__()
        self.tweets = []
        self.client = client
        self._tweet_id = tweet_id
        self.latest = None

    async def get_history(self):
        results = []
        response = await self.client.http.get_tweet_edit_history(self._tweet_id)
        entries = find_objects(response, "type", "TimelineAddEntries", recursive=False, none_value={})
        entries = entries.get('entries', [])
        if not entries:
            _tweet = self.client.tweet_detail(self._tweet_id)
            self.latest = self['latest'] = _tweet
            results.append(_tweet)
        else:
            for entry in entries:
                _tweet = Tweet(self.client, entry, None)

                if entry['entryId'] == self.LATEST_TWEET_ENTRY_ID:
                    self.latest = self['latest'] = _tweet

                results.append(_tweet)
        self.tweets = self["tweets"] = results
        return results

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

    def __repr__(self):
        return "TweetHistory(tweets={}, author={})".format(
            len(self.tweets), self.tweets[0].author
        )


class ScheduledTweets(dict):
    def __init__(self, client):
        super().__init__()
        self._client = client
        self.tweets = []
        self.get_page()

    async def get_page(self):
        res = await self._client.http.get_scheduled_tweets()
        tweets_list = find_objects(res, "scheduled_tweet_list", value=None, none_value=[])

        for tweet in tweets_list:
            try:
                self.tweets.append(ScheduledTweet(self._client, tweet))
            except:
                pass

        self["tweets"] = self.tweets

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

    def __repr__(self):
        return "ScheduledTweets(tweets={})".format(len(self.tweets))

