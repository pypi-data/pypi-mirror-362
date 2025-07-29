import requests


class ThreadsPostCommentCollector:
    """
    A class to collect TikTok posts by keyword.
    """

    # Constants
    RAPID_URL = "https://threads-api4.p.rapidapi.com/api/post/comments"
    RAPID_API_HOST = "threads-api4.p.rapidapi.com"

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
        self.headers = {
            "accept": "application/json",
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.RAPID_API_HOST
        }

    def collect_comments_by_post(self, post_id):

        try:
            comment_list = self._search_comments(post_id)
            print(f"Found {len(comment_list)} comments for post {post_id}")

            comment_full = []
            for cmt in comment_list:
                thread_items = cmt["node"]["thread_items"]

                for thread_item in thread_items:
                    try:
                        comment_info = thread_item["post"]
                        info = {
                            "post_id": post_id,
                            "comment_id": comment_info["pk"],
                            "text": comment_info["caption"]["text"],
                            "create_time": comment_info.get("taken_at"),
                            "num_like": comment_info["like_count"],
                            "num_reply": comment_info["text_post_app_info"]["direct_reply_count"],
                            "user_id": comment_info["user"]["id"],
                            "user_name": comment_info["user"]["username"],
                            "full_name": comment_info["user"]["username"],
                            "avatar_url": comment_info["user"]["profile_pic_url"],
                            "bio": None,
                            "bio_url": None,
                            "num_follower": None,
                            "num_following": None,
                            "num_post": None,
                            "youtube_channel_id": None,
                            "ins_id": None,
                            "live_commerce": None,
                            "region": None,
                        }
                    except Exception as error:
                        print(f"Error processing post: {error}")
                        continue
                    comment_full.append(info)

            return comment_full

        except Exception as e:
            print(f"Error collecting posts for keyword {post_id}: {e}")
            return []

    def _search_comments(self, post_id):
        print(f"Searching comments for post {post_id}")
        retry = 0
        comment_list = []
        cursor = None

        loop_index = 1
        while True:
            try:
                params = {"post_id": post_id, "end_cursor": cursor}
                print(params)
                response = requests.get(
                    self.RAPID_URL,
                    headers=self.headers,
                    params=params)

                data = response.json()
                comments = data["data"]["data"]["edges"]
                cursor = data["data"]["data"]["page_info"]["end_cursor"]
                hasMore = data["data"]["data"]["page_info"]["has_next_page"]
                if len(comments) <= 0:
                    break
                else:
                    comment_list.extend(comments)

                print("hasMore", hasMore)
                if hasMore is not True or not cursor:
                    break
            except Exception as e:
                print(f"Error searching posts: {e}")
                retry += 1
            if retry > self.MAX_POST_COMMENT_RETRY:
                break
            if len(comment_list) > self.MAX_COMMENT_BY_POST:
                break
            loop_index += 1
        return comment_list
