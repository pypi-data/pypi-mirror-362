#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the tiktok-hashtag-collector package.
"""

import unittest
from unittest.mock import patch, MagicMock

from tiktok_hashtag_collector import TiktokHashtagCollector


class TestTiktokHashtagCollector(unittest.TestCase):
    """Test cases for the TiktokHashtagCollector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.collector = TiktokHashtagCollector(country_code="US")

    def test_hashtag_detect(self):
        """Test the _hashtag_detect method."""
        # Test with hashtags
        text = "This is a #test with #multiple #hashtags"
        hashtags = self.collector._hashtag_detect(text)
        self.assertEqual(hashtags, ["test", "multiple", "hashtags"])

        # Test with no hashtags
        text = "This is a test with no hashtags"
        hashtags = self.collector._hashtag_detect(text)
        self.assertEqual(hashtags, [])

        # Test with empty text
        text = ""
        hashtags = self.collector._hashtag_detect(text)
        self.assertEqual(hashtags, [])

    @patch('requests.get')
    def test_get_hashtag_id(self, mock_get):
        """Test the _get_hashtag_id method."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "challenge_list": [
                {
                    "challenge_info": {
                        "cid": "12345"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        # Test with a valid hashtag
        hashtag_id = self.collector._get_hashtag_id("test")
        self.assertEqual(hashtag_id, "12345")

        # Test with an invalid hashtag
        mock_response.json.return_value = {"challenge_list": []}
        hashtag_id = self.collector._get_hashtag_id("invalid")
        self.assertIsNone(hashtag_id)

    @patch('requests.get')
    def test_get_posts(self, mock_get):
        """Test the _get_posts method."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "cursor": 0,
            "aweme_list": [
                {
                    "aweme_id": "12345",
                    "desc": "Test post #test",
                    "create_time": 1609459200,
                    "statistics": {
                        "play_count": 1000,
                        "digg_count": 100,
                        "comment_count": 10,
                        "share_count": 5
                    },
                    "author": {
                        "uid": "user123",
                        "unique_id": "username",
                        "nickname": "User Name",
                        "signature": "User bio",
                        "region": "US"
                    },
                    "video": {
                        "origin_cover": {
                            "url_list": ["https://example.com/image.jpg"]
                        }
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        # Test with a valid hashtag ID
        posts = self.collector._get_posts("12345")
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["aweme_id"], "12345")

        # Test with an empty response
        mock_response.json.return_value = {
            "cursor": 0,
            "aweme_list": []
        }
        posts = self.collector._get_posts("12345")
        self.assertEqual(len(posts), 0)


if __name__ == '__main__':
    unittest.main()
