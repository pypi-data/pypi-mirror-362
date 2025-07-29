import json
import re


def transform_selling_product(data) -> list:
    """
    Transform selling product data from TikTok API response.

    Args:
        data (dict): The product data from the API response

    Returns:
        list: A list of transformed product information
    """
    product_list = []
    if extra := data.get('extra', None):
        for product in json.loads(extra):
            product_info = json.loads(product['extra'])
            _id = product_info.get('product_id', None)
            product_name = product_info.get('title', None)
            thumbnail = product_info.get('cover_url', None)
            seller_id = product_info.get('seller_id', None)
            seller_name = product_info.get('seller_name', None)
            product_list.append({
                'product_id': str(_id),
                'product_title': product_name,
                'thumbnail': thumbnail,
                'seller_id': str(seller_id),
                'seller_name': seller_name
            })
    return product_list


def hashtag_detect(text):
    """
    Detect hashtags in a text.

    Args:
        text (str): The text to detect hashtags in

    Returns:
        list: A list of hashtags
    """
    if not text:
        return []

    hashtags = re.findall(r'#(\w+)', text)
    return hashtags
