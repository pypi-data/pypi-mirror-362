# TikTok Collector

A Python library for collecting TikTok data including hashtags and keywords.

## Installation

```bash
pip install tiktok-collector
```

## Features

- Collect TikTok posts by hashtag
- Collect TikTok posts by keyword
- Collect TikTok Comment by post link
- Configurable API settings
- Rate limiting and error handling

## Usage

### Basic Usage

```python
from tiktok_collector import TiktokHashtagCollector, SparkS3Writer

# Initialize collector
collector = TiktokHashtagCollector(api_key="your_rapidapi_key")

# Collect posts by hashtag
posts = collector.collect_by_hashtag(
    hashtag="python",
    max_posts=100,
    min_likes=1000
)

# Collect posts by keyword


### Configuration

You can configure the collector using environment variables:

```bash
export TIKTOK_API_KEY=your_rapidapi_key
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

## Requirements

- Python 3.7+
- requests
- pandas
- numpy
- python-dotenv
- boto3
- pytz
- httplib2
- sqlalchemy
- openpyxl
- pyspark
- hadoop-aws
- aws-java-sdk-bundle

## License

This project is licensed under the MIT License - see the LICENSE file for details. 