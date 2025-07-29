import requests
import time
import re


class TiktokUserCollector:
    """
    A class to collect TikTok posts by hashtag.
    """

    # Constants
    API_USER_INFO = "https://api.tokapi.online/v1/user/{user_id}?region={region}"
    RAPID_API_HOST = "tokapi"
    NAME_KEYWORD_LIST = [
        "brand",
        "store",
        "official",
        "sctv",
        "entertaiment",
        "shop",
        "news",
        "zalo",
        "bán hàng",
        "mua hàng",
        ".com",
        "phòng khám",
        "cửa hàng",
    ]
    BIO_KEYWORD_LIST = [
        "kinh doanh",
        "store",
        "bán hàng",
        "trung tâm",
        "nhà phân phối",
        "phòng khám",
        "shop",
        "đại lý",
        "sốp",
        "cửa hàng",
    ]

    def __init__(self, api_key, country_code="US", brands = None):
        self.api_key = api_key
        self.country_code = country_code
        self.brands = brands
        self.headers = {
            "x-api-key": self.api_key,
            "x-project-name": self.RAPID_API_HOST
        }

    def collect_user_info(self, user_id):
        try:
            user_info = self._get_user_id(user_id)
            if user_info is None:
                print(f"Could not find username for {user_id}")
                return None

            return user_info

        except Exception as e:
            print(f"Error collecting posts for hashtag {user_id}: {e}")
            return []

    def _get_user_id(self, user_id):
        user_info = None
        url = self.API_USER_INFO.format(
            user_id=user_id, region=self.country_code)
        retry = 0

        while True:
            try:
                response = requests.get(
                    url, headers=self.headers)

                data = response.json()
                user = data.get("user", {})
                seller_id = None
                if user.get("uid"):
                    other_social_networks = []
                    if instagram_username := user.get("ins_id"):
                        other_social_networks.append(
                            {
                                "social_type": "instagram",
                                "username": instagram_username,
                                "social_url": f"https://www.instagram.com/{instagram_username}/",
                            }
                        )

                    if youtube_id := user.get("youtube_channcel_id"):
                        other_social_networks.append(
                            {
                                "social_type": "youtube",
                                "_id": youtube_id,
                                "social_url": f"https://www.youtube.com/channel/{youtube_id}",
                            }
                        )
                    scheduled_live_events = []
                    if len(user.get("scheduled_live_events", [])) > 0:
                        scheduled_live_events = list(
                            map(
                                lambda x: {
                                    **x,
                                    "end_time": x.get("duration", 0) + x.get("start_time", 0),
                                },
                                user.get("scheduled_live_events"),
                            )
                        )
                    if user.get("tab_settings", {}).get("shop_tab", {}).get("shop_schema_v2", None):
                        shop_schema = user.get("tab_settings", {}).get("shop_tab", {}).get("shop_schema_v2", None)
                        m = re.search(r"sellerId=(\d+)", shop_schema)
                        seller_id = m.group(1) if m else None
                        # 'aweme://ec/store?sellerId=7494788045968869899&url_maker=shop_schema_sdk&store_page_version=3'
                    user_info = {
                        "user_id": user.get("uid"),
                        "full_name": user.get("nickname"),
                        "username": user.get("unique_id"),
                        "bio": user.get("signature"),
                        "bio_url": user.get("bio_url", ""),
                        "num_follower": user.get("follower_count"),
                        "num_following": user.get("following_count"),
                        "num_post": user.get("aweme_count"),
                        "num_likes": user.get("num_likes") if user.get("num_likes") else "",
                        "region": user.get("region"),
                        "num_favorite": user.get("favoriting_count"),
                        "has_livestream": True if user.get("room_id") else False,
                        "livestream_info": {
                            "time": int(time.time()),
                            "live_status": "now"
                            } if user.get("room_id") else False,
                        "other_social_networks": other_social_networks,
                        "scheduled_live_events": scheduled_live_events,
                        "ig_id": user.get("ins_id"),
                        "yt_id": user.get("youtube_channcel_id"),
                        "private_account": user.get("secret"),
                        "biz_account_info": user.get("biz_account_info"),
                        "category": user.get("category"),
                        "shop_tab": user.get("tab_settings", {}).get("shop_tab"),
                        "room_id": str(user.get("room_id")) if user.get("room_id") else "",
                        "account_type": self._check_kol_profile(user, seller_id),
                        "mk_acount_type": self._check_kol_account_type(user),
                        "mk_profile_type": self._check_kol_profile_type(user.get("follower_count")),
                        "seller_id": seller_id
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

    def _check_kol_profile(self, user, seller_id):
        kol = 'Creator'
        if seller_id:
            return 'Seller'
        # if isinstance(user.get("seller_id"), str) and user.get("seller_id"):
        #     return True
        # if isinstance(user.get("unique_id"), str):
        #     if any(
        #         keyword.lower == user.get("unique_id").lower()
        #         for keyword in self.brands
        #     ):
        #         return "Official brand"
        #     if any(
        #         keyword in user.get("unique_id").lower()
        #         for keyword in self.NAME_KEYWORD_LIST
        #     ):
        #         return "Business Page"
        # if isinstance(user.get("nickname"), str):
        #     if any(
        #         keyword in user.get("nickname").lower()
        #         for keyword in self.NAME_KEYWORD_LIST
        #     ):
        #         return "Business Page"
        # if isinstance(user.get("signature"), str):
        #     if any(
        #         keyword in user["signature"].lower() for keyword in self.BIO_KEYWORD_LIST
        #     ):
        #         return "Business Page"

        return kol
    
    def _check_kol_account_type(self, user):
        kol = 'Creator'
        if isinstance(user.get("unique_id"), str):
            if any(
                keyword.lower == user.get("unique_id").lower()
                for keyword in self.brands
            ):
                return "Official brand"
            if any(
                keyword in user.get("unique_id").lower()
                for keyword in self.NAME_KEYWORD_LIST
            ):
                return "Business Page"
        if isinstance(user.get("nickname"), str):
            if any(
                keyword in user.get("nickname").lower()
                for keyword in self.NAME_KEYWORD_LIST
            ):
                return "Business Page"
        if isinstance(user.get("signature"), str):
            if any(
                keyword in user["signature"].lower() for keyword in self.BIO_KEYWORD_LIST
            ):
                return "Business Page"

        return kol

    def _check_kol_profile_type(self, follower):
        if follower:
            if follower > 1000000:
                return ">1M"
            elif follower > 300000:
                return ">300K"
            elif follower > 30000:
                return ">30K"
            elif follower > 1000:
                return "<30K"
        return "<1K"
