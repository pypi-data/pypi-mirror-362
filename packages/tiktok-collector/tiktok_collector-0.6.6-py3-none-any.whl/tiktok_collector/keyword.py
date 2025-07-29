import datetime
import requests
import json
from .utils import transform_selling_product, hashtag_detect
import time


class TiktokKeywordCollector:
    """
    A class to collect TikTok posts by keyword.
    """

    # Constants
    RAPID_URL_SEARCH = "https://api.tokapi.online/v1/search/post"
    RAPID_API_HOST = "tokapi"

    def __init__(
        self,
        api_key,
        country_code="US",
        max_post_by_keyword=100,
        max_keyword_post_retry=3,
    ):
        """
        Initialize the collector with an API key and configuration.

        Args:
            api_key (str): Your RapidAPI key for TikTok API
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
            "x-api-key": self.api_key,
            "x-project-name": self.RAPID_API_HOST,
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
                i = i.get("aweme_info")
                author = i["author"]
                try:
                    display_url = (
                        i.get("video", {}).get("origin_cover", {}).get("url_list")[-1]
                    )
                except Exception as e:
                    print(f"Error getting display_url: {e}")
                    display_url = ""
                try:
                    duration = i["video"]["duration"] if "duration" in i["video"] else 0
                    duration_ = int(duration) / 1000
                    products = []
                    live_events = []
                    if anchors := i.get("anchors", None):
                        for anchor in anchors:
                            if (
                                anchor.get("component_key", None)
                                == "anchor_complex_shop"
                            ):
                                products = products + transform_selling_product(anchor)
                            if anchor.get("component_key", None) == "anchor_live_event":
                                extra = json.loads(anchor.get("extra", "{}"))
                                live_event_id = extra.get("third_id", None)
                                timestamp = extra.get("time", None)
                                live_events.append(
                                    {
                                        "event_id": live_event_id,
                                        "time_start": timestamp,
                                    }
                                )
                    create_date = (
                        datetime.datetime.utcfromtimestamp(i["create_time"]).strftime(
                            "%m/%d/%Y"
                        )
                        if "create_time" in i and i["create_time"]
                        else ""
                    )
                    content_type = "VIDEO"
                    if i.get("content_type") == "image":
                        content_type = "IMAGE"

                    brand_partnership = 0
                    if i.get("commerce_info", {}).get("branded_content_type") == 1:
                        brand_partnership = 1
                    post_info = {
                        "search_method": "Keyword",
                        "input_kw_hst": keyword,
                        "post_id": i["aweme_id"],
                        "post_link": f"www.tiktok.com/@{author['uid']}/video/{i['aweme_id']}",
                        "caption": i["desc"],
                        "created_date": create_date,
                        "num_view": i["statistics"]["play_count"],
                        "num_like": i["statistics"]["digg_count"],
                        "num_comment": i["statistics"]["comment_count"],
                        "num_share": i["statistics"]["share_count"],
                        "num_buzz": i["statistics"]["comment_count"]
                        + i["statistics"]["share_count"],
                        "num_save": i["statistics"]["collect_count"],
                        "target_country": i["region"],
                        "taken_at_timestamp": int(i["create_time"]),
                        "display_url": display_url,
                        "hashtag": (
                            ", ".join(self._hashtag_detect(i["desc"]))
                            if i["desc"]
                            else ""
                        ),
                        "hashtags": self._hashtag_detect(i["desc"]),
                        "user_id": author["uid"],
                        "username": author["unique_id"],
                        "avatar_url": None,
                        "bio": author["signature"] if author.get("signature") else "",
                        "full_name": author["nickname"],
                        "music_id": i["music"]["id"] if i.get("music") else "",
                        "music_name": i["music"]["title"] if i.get("music") else "",
                        "duration": duration_,
                        "products": products,
                        "live_events": live_events,
                        "content_type": content_type,
                        "brand_partnership": brand_partnership,
                    }
                except Exception as error:
                    print(f"Error processing post: {error}")
                    continue
                content_full.append(post_info)

            return content_full

        except Exception as e:
            print(f"Error collecting posts for keyword {keyword}: {e}")
            return []

    def _search_posts(self, keyword, country_code=None):
        """
        Search posts for a given keyword.

        Args:
            keyword (str): The keyword to search for
            country_code (str, optional): The country code to filter by

        Returns:
            list: A list of posts
        """
        if country_code is None:
            country_code = self.country_code

        print(f"Searching posts for keyword {keyword}")
        posts = []

        publish_times = [0, 7, 30, 90, 180]

        for publish_time in publish_times:
            retry = 0
            cursor = 0
            loop_index = 1
            while True:
                try:
                    params = {
                        "keyword": keyword,
                        "count": 30,
                        "region": country_code.upper(),
                        "offset": cursor,
                        "sort_type": 3,
                        "publish_time": publish_time,
                    }
                    print(params)
                    response = requests.get(
                        self.RAPID_URL_SEARCH, headers=self.headers, params=params
                    )

                    data = response.json()
                    cursor = data["cursor"]
                    aweme_list = data["search_item_list"]
                    has_more = data["has_more"]

                    if aweme_list is None or len(aweme_list) == 0:
                        break
                    else:
                        posts.extend(aweme_list)

                    if not has_more:
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
