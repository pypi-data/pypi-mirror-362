import datetime
import requests
import json
from .utils import transform_selling_product, hashtag_detect
import time


class TiktokBrandCollector:
    """
    A class to collect TikTok posts by hashtag.
    """

    # Constants
    API_USER_INFO = "https://api.tokapi.online/v1/user/@{username}"
    API_POST_LIST = "https://api.tokapi.online/v1/post/user/{user_id}/posts"
    RAPID_API_HOST = "tokapi"

    def __init__(self, api_key, country_code="US",
                 max_post_by_brand=100,
                 max_brand_post_retry=3,
                 max_profile_retry=3):
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
        self.MAX_POST_BY_HASHTAG = max_post_by_brand
        self.MAX_HASHTAG_POST_RETRY = max_brand_post_retry
        self.MAX_PROFILE_RETRY = max_profile_retry
        self.headers = {
            "x-api-key": self.api_key,
            "x-project-name": self.RAPID_API_HOST
        }

    def collect_posts_by_brand(self, username):
        """
        Collect posts for a single hashtag.

        Args:
            hashtag_key (str): The hashtag to collect posts for

        Returns:
            pandas.DataFrame: A DataFrame containing the collected posts
        """
        try:
            collected_posts = []
            user_info = self._get_user_id(username)
            if user_info is None:
                print(f"Could not find username for {username}")
                return collected_posts, user_info

            user_id = user_info.get("user_id")
            content_list, user_info = self._get_posts(user_id)
            print(f"Found {len(collected_posts)} posts for user {username}")

            content_full = []
            for i in content_list:
                try:
                    display_url = i.get("display_url")[-1]
                except Exception as e:
                    print(f"Error getting display_url: {e}")
                    display_url = ""
                try:
                    create_date = datetime.datetime.utcfromtimestamp(
                        i["create_time"]).strftime("%m/%d/%Y") if 'create_time' in i and i["create_time"] else ""
                    post_info = {
                        "search_method": "Brand",
                        "input_kw_hst": username,
                        **i,
                        "created_date": create_date,
                        "display_url": display_url,
                        "hashtag": ", ".join(self._hashtag_detect(i['desc'])) if i['desc'] else "",
                        "hashtags": self._hashtag_detect(i['desc']),
                        "target_country": user_info.get("region"),
                        "user_id": user_info.get("user_id"),
                        "username": username,
                        "bio": user_info.get("bio"),
                        "full_name": user_info.get("full_name"),
                        "num_follower": user_info.get("num_follower"),
                        "avatar_url": None,
                    }
                except Exception as error:
                    print(f"Error processing post: {error}")
                    continue
                content_full.append(post_info)

            return content_full

        except Exception as e:
            print(f"Error collecting posts for hashtag {username}: {e}")
            return []

    def _get_user_id(self, username):
        user_info = None
        url = self.API_USER_INFO.format(
            username=username)
        retry = 0

        while True:
            try:
                response = requests.get(
                    url, headers=self.headers)

                data = response.json()
                user = data.get("user", {})
                if user.get("uid"):
                    user_info = {
                        "user_id": user.get("uid"),
                        "full_name": user.get("nickname"),
                        "bio": user.get("signature"),
                        "num_follower": user.get("follower_count"),
                        "region": user.get("region"),
                    }
                    break
                if (response.status_code != 200):
                    raise Exception('Error request')

            except Exception as e:
                print("Load user id error", e)

            retry += 1
            if retry > 3:
                break
        return user_info

    def _get_posts(self, user_id, country_code=None):
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

        print(f"Getting posts for user_id {user_id}")
        url = self.API_POST_LIST.format(user_id=user_id)
        headers = self.RAPID_TOKAPI_HEADER
        retry = 0
        posts = []

        loop_index = 1
        while True:
            try:
                params = {"count": 30, "region": country_code.upper() if country_code else None}
                print(params)
                response = requests.get(
                    url, headers=self.headers, params=params)

                response = requests.get(url, headers=headers, params=params)

                data = response.json()
                collected_post = data.get("aweme_list")
                transformed_posts = []
                if isinstance(collected_post, list) and len(collected_post) > 0:
                    transformed_posts = [self.clean_post(
                        item) for item in collected_post]

                posts += transformed_posts
                print(len(transformed_posts))
                if not data.get('max_cursor') or not isinstance(data.get('max_cursor'), int):
                    break

                params['offset'] = data.get('max_cursor')
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

    @staticmethod
    def clean_post(item):
        author = item["author"]
        duration = item["video"]["duration"] if "duration" in item["video"] else 0
        duration_ = int(duration)/1000
        products = []
        live_events = []
        if anchors := item.get('anchors', None):
            for anchor in anchors:
                if anchor.get('component_key', None) == 'anchor_complex_shop':
                    products = products + transform_selling_product(
                        anchor)
                if anchor.get('component_key', None) == 'anchor_live_event':
                    extra = json.loads(anchor.get('extra', '{}'))
                    live_event_id = extra.get('third_id', None)
                    timestamp = extra.get('time', None)
                    live_events.append(
                        {
                            "event_id": live_event_id,
                            "time_start": timestamp,
                        }
                    )
        return {
            "post_id": item.get("aweme_id"),
            "post_link": f"www.tiktok.com/@{author['uid']}/video/{item['aweme_id']}",
            "caption": item.get("desc"),
            "num_comment": item.get("statistics", {}).get("comment_count"),
            "num_like": item.get("statistics", {}).get("digg_count"),
            "num_view": item.get("statistics", {}).get("play_count"),
            "num_share": item.get("statistics", {}).get("share_count"),
            "num_save": item.get("statistics", {}).get("collect_count"),
            "taken_at_timestamp": int(item.get("create_time")),
            "display_url": item.get("video", {}).get("origin_cover", {}).get("url_list"),
            "region": item.get("region"),
            "username": item.get("author", {}).get("unique_id"),
            "user_id": item.get("author", {}).get("uid"),
            "music_id": item["music"]["id"] if item["music"] else "",
            "music_name": item["music"]["title"] if item["music"] else "",
            "duration": duration_,
            "products": products,
            "live_events": live_events,
        }
