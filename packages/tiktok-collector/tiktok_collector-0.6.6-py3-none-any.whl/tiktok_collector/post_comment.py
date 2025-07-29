import requests


class TiktokPostCommentCollector:
    """
    A class to collect TikTok posts by keyword.
    """

    # Constants
    NO_WATERMARK_API_URL = (
        "https://tiktok-video-no-watermark2.p.rapidapi.com/comment/list"
    )
    NO_WATERMARK_RAPID_API_HOST = "tiktok-video-no-watermark2.p.rapidapi.com"

    API_URL = "https://api.tokapi.online/v1/post/{post_id}/comments"
    RAPID_API_HOST = "tokapi"

    def __init__(self, api_key, max_comment_by_post=100, max_post_comment_retry=3):
        """
        Initialize the collector with an API key and configuration.

        Args:
            api_key (str): Your RapidAPI key for TikTok API
            country_code (str): The country code to filter posts by (default: "US")
            max_post_by_keyword (int): Maximum number of posts to collect per keyword (default: 100)
            max_keyword_post_retry (int): Maximum number of retries for keyword post collection (default: 3)
        """
        self.api_key = api_key
        self.MAX_COMMENT_BY_POST = max_comment_by_post
        self.MAX_POST_COMMENT_RETRY = max_post_comment_retry
        self.no_watermark_headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.NO_WATERMARK_RAPID_API_HOST,
        }

        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key,
            "x-project-name": self.RAPID_API_HOST,
        }

    def collect_comments_by_post_no_watermark2(self, post_id):

        try:
            comment_list = self._search_comments(post_id)
            print(f"Found {len(comment_list)} comments for post {post_id}")

            comment_full = []
            for cmt in comment_list:
                try:
                    info = {
                        "post_id": post_id,
                        "comment_id": cmt.get("id"),
                        "text": cmt.get("text"),
                        "create_time": cmt.get("create_time"),
                        "num_like": cmt.get("digg_count"),
                        "num_reply": cmt.get("reply_total"),
                        "user_id": cmt.get("user", {}).get("user_id"),
                        "user_name": cmt.get("user", {}).get("unique_id"),
                        "full_name": cmt.get("user", {}).get("nickname", None),
                        "avatar_url": cmt.get("user", {}).get("avatar", None),
                        "bio": cmt.get("user", {}).get("bio", None),
                        "bio_url": cmt.get("user", {}).get("bio_url", None),
                        "num_follower": cmt.get("user", {}).get("follower_count", None),
                        "num_following": cmt.get("user", {}).get(
                            "following_count", None
                        ),
                        "num_post": cmt.get("user", {}).get("aweme_count", None),
                        "youtube_channel_id": cmt.get("user", {}).get(
                            "youtube_channel_id", None
                        ),
                        "ins_id": cmt.get("user", {}).get("ins_id", None),
                        "live_commerce": cmt.get("user", {}).get("live_commerce", None),
                        "region": cmt.get("user", {}).get("region", None),
                    }
                except Exception as error:
                    print(f"Error processing post: {error}")
                    continue
                comment_full.append(info)

            return comment_full

        except Exception as e:
            print(f"Error collecting posts for keyword {post_id}: {e}")
            return []

    def _search_comments_no_watermark2(self, post_id):
        print(f"Searching comments for post {post_id}")
        retry = 0
        comment_list = []
        cursor = 0

        loop_index = 1
        while True:
            try:
                querystring = {
                    "url": f"https://www.tiktok.com/@tiktok/video/{post_id}",
                    "count": "50",
                    "cursor": cursor,
                }
                print(querystring)
                response = requests.get(
                    self.NO_WATERMARK_API_URL, headers=self.headers, params=querystring
                )

                data = response.json()["data"]
                cursor = data["cursor"]
                comments = data["comments"]
                if len(comments) <= 0:
                    break
                else:
                    comment_list.extend(comments)
                print(f"Total posts {loop_index}: {len(comment_list)}")
            except Exception as e:
                print(f"Error searching posts: {e}")
                retry += 1
            if retry > self.MAX_POST_COMMENT_RETRY:
                break
            if len(comment_list) > self.MAX_COMMENT_BY_POST:
                break
            loop_index += 1
        return comment_list

    def collect_comments_by_post(self, post_id, country_code="GB"):

        try:
            comment_list = self._search_comments(post_id, country_code)
            print(f"Found {len(comment_list)} comments for post {post_id}")

            comment_full = []
            for cmt in comment_list:
                try:
                    info = {
                        "post_id": post_id,
                        "comment_id": cmt.get("cid"),
                        "text": cmt.get("text"),
                        "create_time": cmt.get("create_time"),
                        "num_like": cmt.get("digg_count"),
                        "num_reply": cmt.get("reply_comment_total") or 0,
                        "user_id": cmt.get("user", {}).get("uid"),
                        "user_name": cmt.get("user", {}).get("unique_id"),
                        "full_name": cmt.get("user", {}).get("nickname", None),
                        "avatar_url": cmt.get("user", {}).get("avatar", None),
                        "bio": cmt.get("user", {}).get("signature", None),
                        "bio_url": cmt.get("user", {}).get("bio_url", None),
                        "num_follower": cmt.get("user", {}).get("follower_count", None),
                        "num_following": cmt.get("user", {}).get(
                            "following_count", None
                        ),
                        "num_post": cmt.get("user", {}).get("aweme_count", None),
                        "youtube_channel_id": cmt.get("user", {}).get(
                            "youtube_channel_id", None
                        ),
                        "ins_id": cmt.get("user", {}).get("ins_id", None),
                        "live_commerce": cmt.get("user", {}).get("live_commerce", None),
                        "region": cmt.get("user", {}).get("region", None),
                    }
                except Exception as error:
                    print(f"Error processing post: {error}")
                    continue
                comment_full.append(info)

            return comment_full

        except Exception as e:
            print(f"Error collecting posts for keyword {post_id}: {e}")
            return []

    def _search_comments(self, post_id, country_code="GB"):
        print(f"Searching comments for post {post_id}")
        retry = 0
        comment_list = []
        cursor = 0

        loop_index = 1
        while True:
            try:
                querystring = {
                    "count": "50",
                    "offset": cursor,
                    "region": country_code,
                    "type": "Top",
                }
                print(querystring)
                response = requests.get(
                    self.API_URL.format(post_id=post_id),
                    headers=self.headers,
                    params=querystring,
                )

                data = response.json()
                cursor = data["cursor"]
                comments = data["comments"]
                if len(comments) <= 0:
                    break
                else:
                    comment_list.extend(comments)
                print(f"Total posts {loop_index}: {len(comment_list)}")
            except Exception as e:
                print(f"Error searching posts: {e}")
                retry += 1
            if retry > self.MAX_POST_COMMENT_RETRY:
                break
            if len(comment_list) > self.MAX_COMMENT_BY_POST:
                break
            loop_index += 1
        return comment_list
