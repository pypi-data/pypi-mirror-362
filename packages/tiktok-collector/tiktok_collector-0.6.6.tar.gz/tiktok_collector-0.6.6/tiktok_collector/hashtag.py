import datetime
import requests
import json
from .utils import transform_selling_product, hashtag_detect
import time


class TiktokHashtagCollector:
    """
    A class to collect TikTok posts by hashtag.
    """

    # Constants
    RAPID_URL_COLLECT_HASHTAG = "https://api.tokapi.online/v1/search/hashtag"
    RAPID_URL_COLLECT_POST_BY_HASHTAG = (
        "https://api.tokapi.online/v1/hashtag/posts/{hashtag_id}"
    )
    RAPID_API_HOST = "tokapi"

    def __init__(
        self,
        api_key,
        country_code="US",
        max_post_by_hashtag=100,
        max_hashtag_post_retry=3,
        max_profile_retry=3,
    ):
        """
        Initialize the collector with an API key and configuration.

        Args:
            api_key (str): Your RapidAPI key for TikTok API
            country_code (str): The country code to filter posts by (default: "US")
            max_post_by_hashtag (int): Maximum number of posts to collect per hashtag (default: 100)
            max_hashtag_post_retry (int): Maximum number of retries for hashtag post collection (default: 3)
            max_profile_retry (int): Maximum number of retries for profile collection (default: 3)
        """
        self.api_key = api_key
        self.country_code = country_code
        self.MAX_POST_BY_HASHTAG = max_post_by_hashtag
        self.MAX_HASHTAG_POST_RETRY = max_hashtag_post_retry
        self.MAX_PROFILE_RETRY = max_profile_retry
        self.headers = {
            "x-api-key": self.api_key,
            "x-project-name": self.RAPID_API_HOST,
        }

    def collect_posts_by_hashtag(self, hashtag_key):
        """
        Collect posts for a single hashtag.

        Args:
            hashtag_key (str): The hashtag to collect posts for

        Returns:
            pandas.DataFrame: A DataFrame containing the collected posts
        """
        try:
            hashtag_id = self._get_hashtag_id(hashtag_key)
            if hashtag_id is None:
                print(f"Could not find hashtag ID for {hashtag_key}")
                return []

            content_list = self._get_posts(hashtag_id)
            print(f"Found {len(content_list)} posts for hashtag {hashtag_key}")

            content_full = []
            for i in content_list:
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
                        "search_method": "Hashtag",
                        "input_kw_hst": hashtag_key,
                        "post_id": i["aweme_id"],
                        "post_link": f"www.tiktok.com/@{author['uid']}/video/{i['aweme_id']}",
                        "caption": i["desc"],
                        "hashtag": (
                            ", ".join(self._hashtag_detect(i["desc"]))
                            if i["desc"]
                            else ""
                        ),
                        "hashtags": self._hashtag_detect(i["desc"]),
                        "created_date": create_date,
                        "num_view": i["statistics"]["play_count"],
                        "num_like": i["statistics"]["digg_count"],
                        "num_comment": i["statistics"]["comment_count"],
                        "num_share": i["statistics"]["share_count"],
                        "num_buzz": i["statistics"]["comment_count"]
                        + i["statistics"]["share_count"],
                        "num_save": i["statistics"]["collect_count"],
                        "target_country": author["region"],
                        "user_id": author["uid"],
                        "username": author["unique_id"],
                        "bio": author["signature"] if author.get("signature") else "",
                        "full_name": author["nickname"],
                        "avatar_url": None,
                        "display_url": display_url,
                        "taken_at_timestamp": int(i["create_time"]),
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
            print(f"Error collecting posts for hashtag {hashtag_key}: {e}")
            return []

    def _get_hashtag_id(self, hashtag, country_code=None):
        """
        Get the hashtag ID for a given hashtag.

        Args:
            hashtag (str): The hashtag to get the ID for
            country_code (str, optional): The country code to filter by

        Returns:
            str: The hashtag ID or None if not found
        """
        if country_code is None:
            country_code = self.country_code

        retry = 0
        params = {"keyword": hashtag, "count": "10", "region": country_code.upper()}
        data = None
        print(f"Getting hashtag ID for {hashtag}")

        while True:
            try:
                response = requests.get(
                    self.RAPID_URL_COLLECT_HASHTAG, headers=self.headers, params=params
                )

                data = response.json()
                if data.get("challenge_list") and len(data["challenge_list"]) > 0:
                    data = data["challenge_list"][0]["challenge_info"]["cid"]
                    break
            except Exception as e:
                print(f"Error getting hashtag ID: {e}")
                retry += 1
            print(f"Retry {retry}")
            if retry > self.MAX_PROFILE_RETRY:
                break
        return data

    def _get_posts(self, hashtag_id, country_code=None):
        """
        Get posts for a given hashtag ID.

        Args:
            hashtag_id (str): The hashtag ID to get posts for
            country_code (str, optional): The country code to filter by

        Returns:
            list: A list of posts
        """
        if country_code is None:
            country_code = self.country_code

        print(f"Getting posts for hashtag ID {hashtag_id}")
        url = self.RAPID_URL_COLLECT_POST_BY_HASHTAG.format(hashtag_id=hashtag_id)
        retry = 0
        posts = []
        cursor = 0

        loop_index = 1
        while True:
            try:
                params = {"count": 20, "region": country_code.upper(), "offset": cursor}
                print(params)
                response = requests.get(url, headers=self.headers, params=params)

                data = response.json()
                cursor = data["cursor"]
                aweme_list = data["aweme_list"]
                if len(aweme_list) <= 0:
                    break
                else:
                    posts.extend(aweme_list)
                print(f"Total posts {loop_index}: {len(posts)}")
            except Exception as e:
                print(f"Error getting posts: {e}")
                retry += 1
            if retry > self.MAX_HASHTAG_POST_RETRY:
                break
            if len(posts) > self.MAX_POST_BY_HASHTAG:
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
