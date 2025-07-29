from setuptools import setup, find_packages

setup(
    name="tiktok-collector",
    version="0.6.6",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
        "numpy>=1.19.0",
        "python-dotenv>=0.19.0",
        "boto3>=1.26.0",
        "pytz>=2021.1",
        "httplib2>=0.20.0",
        "sqlalchemy>=1.4.0",
        "openpyxl>=3.1.0",
        "pyspark>=3.3.0",
    ],
    author="Dong Hoang",
    author_email="donghoang@example.com",
    description="A Python library for collecting TikTok data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tiktok-collector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
