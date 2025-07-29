import datetime
import requests
import json
from .utils import transform_selling_product, hashtag_detect
import time


class TiktokPostRecentCollector:
    """
    A class to collect TikTok posts by hashtag.
    """

    # Constants
    API_POST_LIST = "https://api.tokapi.online/v1/post/user/{user_id}/posts"
    RAPID_API_HOST = "tokapi"

    def __init__(self, api_key, country_code="US"):
        self.api_key = api_key
        self.country_code = country_code
        self.headers = {
            "x-api-key": self.api_key,
            "x-project-name": self.RAPID_API_HOST
        }

    def collect_posts_by_recent(self, user_id):
        try:
            content_list = self._get_posts(user_id)
            print(f"Found {len(content_list)} posts for user {user_id}")

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
                        **i,
                        "created_date": create_date,
                        "display_url": display_url,
                        "hashtag": ", ".join(self._hashtag_detect(i['caption'])) if i['caption'] else "",
                        "hashtags": self._hashtag_detect(i['caption']),
                    }
                except Exception as error:
                    print(f"Error processing post: {error}")
                    continue
                content_full.append(post_info)

            return content_full

        except Exception as e:
            print(f"Error collecting posts for hashtag {user_id}: {e}")
            return []

    def _get_posts(self, user_id, country_code=None):
        if country_code is None:
            country_code = self.country_code

        print(f"Getting posts for user_id {user_id}")
        url = self.API_POST_LIST.format(user_id=user_id)
        retry = 0
        posts = []

        loop_index = 1
        params = {"count": 30, "region": country_code.upper() if country_code else None}
        while True:
            try:
                print(params)
                response = requests.get(
                    url, headers=self.headers, params=params)

                data = response.json()
                collected_post = data.get("aweme_list")
                transformed_posts = []
                if isinstance(collected_post, list) and len(collected_post) > 0:
                    transformed_posts = [self.clean_post(
                        item) for item in collected_post]

                return transformed_posts
            except Exception as e:
                print(f"Error getting posts: {e}")
                retry += 1
            if retry > 3:
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
        is_ecommerce_video = False
        if item.get("ecommerce_product_info"):
            ecommerce_info = json.loads(item["ecommerce_product_info"])
            is_ecommerce_video = ecommerce_info.get(
                "is_ecommerce_video", False
            )
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
            "taken_at_timestamp": int(item.get("create_time")),
            "display_url": item.get("video", {}).get("origin_cover", {}).get("url_list"),
            "region": item.get("region"),
            "username": item.get("author", {}).get("unique_id"),
            "user_id": item.get("author", {}).get("uid"),
            "music_id": item["music"]["id"] if item["music"] else "",
            "music_name": item["music"]["title"] if item["music"] else "",
            "duration": duration_,
            "have_ecommerce_product": True if len(products) > 0 else False,
            "ecommerce_product_count": len(products),
            "is_ecommerce_video": is_ecommerce_video,
            "products": products,
            "live_events": live_events,
        }
