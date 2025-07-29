import datetime
import requests
from .utils import hashtag_detect
import time


class ThreadsKeywordCollector:
    """
    A class to collect Threads posts by keyword.
    """

    # Constants
    RAPID_URL = "https://threads-api4.p.rapidapi.com/api/search/top"
    RAPID_API_HOST = "threads-api4.p.rapidapi.com"

    def __init__(
        self,
        api_key,
        country_code="VN",
        max_post_by_keyword=100,
        max_keyword_post_retry=3,
    ):
        """
        Initialize the collector with an API key and configuration.

        Args:
            api_key (str): Your RapidAPI key for Threads API
            country_code (str): The country code to filter posts by (default: "US")
            max_post_by_keyword (int): Maximum number of posts to collect per keyword (default: 100)
            max_keyword_post_retry (int): Maximum number of retries for keyword post collection (default: 3)
        """
        self.api_key = api_key
        self.country_code = country_code
        self.MAX_POST_BY_KEYWORD = max_post_by_keyword
        self.MAX_KEYWORD_POST_RETRY = max_keyword_post_retry
        self.headers = {
            "accept": "application/json",
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.RAPID_API_HOST,
        }

    def collect_posts_by_keyword(self, keyword):
        """
        Collect posts for a single keyword.

        Args:
            keyword (str): The keyword to collect posts for

        Returns:
            pandas.DataFrame: A DataFrame containing the collected posts
        """
        try:
            content_list = self._search_posts(keyword)
            print(f"Found {len(content_list)} posts for keyword {keyword}")

            content_full = []
            for i in content_list:
                try:

                    user_id = i["node"]["thread"]["thread_items"][0]["post"]["user"][
                        "id"
                    ]
                    username = i["node"]["thread"]["thread_items"][0]["post"]["user"][
                        "username"
                    ]
                    post_code = i["node"]["thread"]["thread_items"][0]["post"]["code"]
                    post_id = i["node"]["thread"]["thread_items"][0]["post"]["pk"]
                    link_post = f"https://www.threads.net/@{username}/post/{post_code}"
                    caption = i["node"]["thread"]["thread_items"][0]["post"]["caption"][
                        "text"
                    ]
                    num_like = i["node"]["thread"]["thread_items"][0]["post"][
                        "like_count"
                    ]
                    reply_count = (
                        i["node"]["thread"]["thread_items"][0]["post"][
                            "text_post_app_info"
                        ]["direct_reply_count"]
                        or 0
                    )
                    repost_count = (
                        i["node"]["thread"]["thread_items"][0]["post"][
                            "text_post_app_info"
                        ]["repost_count"]
                        or 0
                    )
                    taken_at = i["node"]["thread"]["thread_items"][0]["post"][
                        "taken_at"
                    ]
                    date = datetime.datetime.fromtimestamp(taken_at)
                    post_info = {
                        "search_method": "Keyword",
                        "input_kw_hst": keyword,
                        "post_id": post_id,
                        "post_link": link_post,
                        "caption": caption,
                        "created_date": date,
                        "num_view": 0,
                        "num_like": num_like,
                        "num_comment": reply_count,
                        "num_share": repost_count,
                        "num_buzz": reply_count + repost_count,
                        "target_country": self.country_code,
                        "taken_at_timestamp": taken_at,
                        "display_url": None,
                        "hashtag": (
                            ", ".join(self._hashtag_detect(caption)) if caption else ""
                        ),
                        "hashtags": self._hashtag_detect(caption),
                        "user_id": user_id,
                        "username": username,
                        "avatar_url": None,
                        "bio": "",
                        "full_name": username,
                        "music_id": None,
                        "music_name": None,
                        "duration": None,
                        "products": [],
                        "live_events": [],
                        "content_type": "POST",
                        "brand_partnership": 0,
                    }

                except Exception as error:
                    print(f"Error processing post: {error}")
                    continue
                content_full.append(post_info)

            return content_full

        except Exception as e:
            print(f"Error collecting posts for keyword {keyword}: {e}")
            return []

    def _search_posts(self, keyword):
        """
        Search posts for a given keyword.

        Args:
            keyword (str): The keyword to search for

        Returns:
            list: A list of posts
        """

        print(f"Searching posts for keyword {keyword}")
        retry = 0
        posts = []
        cursor = ""

        loop_index = 1
        while True:
            try:
                params = {"query": keyword, "end_cursor": cursor}
                print(params)
                response = requests.get(
                    self.RAPID_URL, headers=self.headers, params=params
                )

                data = response.json()
                cursor = data["data"]["searchResults"]["page_info"]["end_cursor"]
                aweme_list = data["data"]["searchResults"]["edges"]
                hasMore = data["data"]["searchResults"]["page_info"]["has_next_page"]
                if len(aweme_list) <= 0:
                    break
                else:
                    posts.extend(aweme_list)
                if hasMore is not True or not cursor:
                    break
                print(f"Total posts {loop_index}: {len(posts)}")
            except Exception as e:
                print(f"Error searching posts: {e}")
                retry += 1
            if retry > self.MAX_KEYWORD_POST_RETRY:
                break
            if len(posts) > self.MAX_POST_BY_KEYWORD:
                break
            loop_index += 1
            time.sleep(2)
        return posts

    @staticmethod
    def _hashtag_detect(text):
        """
        Detect hashtags in a text.

        Args:
            text (str): The text to detect hashtags in

        Returns:
            list: A list of hashtags
        """
        return hashtag_detect(text)
