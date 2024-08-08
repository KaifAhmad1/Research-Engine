# datafetching.py

import logging
from typing import List, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from apify_client import ApifyClient
from pydantic import BaseModel, Field, HttpUrl
from langchain.tools import DuckDuckGoSearchRun
from exa_py import Exa
from config.apikeys import APIFY_API_KEY, EXA_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Apify client
apify_client = ApifyClient(APIFY_API_KEY)
# Configure requests session with retries and timeouts
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))
session.mount('http://', HTTPAdapter(max_retries=retries))

# Define Pydantic models for Structured output 
class Website(BaseModel):
    url: HttpUrl

class SearchTerm(BaseModel):
    term: str

class InputData(BaseModel):
    websites: List[Website]
    search_terms: List[SearchTerm]

class NewsArticle(BaseModel):
    title: str
    url: HttpUrl
    snippet: str

class Tweet(BaseModel):
    text: str
    url: HttpUrl

class CVEData(BaseModel):
    id: str
    description: str
    published: str
    modified: str
    cvss: float

class ExaData(BaseModel):
    title: str
    url: HttpUrl
    snippet: str

class DuckDuckGoResult(BaseModel):
    title: str
    url: HttpUrl
    snippet: str

class OutputData(BaseModel):
    web_data: List[dict] = Field(default_factory=list)
    tweet_data: List[Tweet] = Field(default_factory=list)
    news_data: List[NewsArticle] = Field(default_factory=list)
    cve_data: List[CVEData] = Field(default_factory=list)
    exa_data: List[ExaData] = Field(default_factory=list)
    duckduckgo_data: List[DuckDuckGoResult] = Field(default_factory=list)

# Data collection functions
def scrape_websites(websites: List[Website]) -> List[dict]:
    results = []
    for website in websites:
        try:
            response = session.get(website.url, timeout=10)
            response.raise_for_status()
            results.append({"url": website.url, "content": response.text})
        except Exception as e:
            logger.error(f"Error scraping {website.url}: {str(e)}")
    return results

def fetch_tweets(query: SearchTerm, max_tweets: int = 100) -> List[Tweet]:
    try:
        run = apify_client.actor("apidojo/tweet-scraper").call(
            run_input={"searchTerms": [query.term], "maxTweets": max_tweets, "languageCode": "en"}
        )
        return [Tweet(text=item['text'], url=item['url']) for item in apify_client.dataset(run["defaultDatasetId"]).list_items().items]
    except Exception as e:
        if "Monthly usage hard limit exceeded" in str(e):
            logger.warning("Monthly usage hard limit exceeded. Please upgrade your subscription or contact support@apify.com")
        else:
            logger.error(f"Error fetching tweets: {str(e)}")
        return []

def fetch_cve_data() -> List[CVEData]:
    retries = 3
    for attempt in range(retries):
        try:
            response = session.get("https://cve.circl.lu/api/last", timeout=30)
            response.raise_for_status()
            return [CVEData(**item) for item in response.json()]
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout error. Retrying ({attempt + 1}/{retries})...")
        except Exception as e:
            logger.error(f"Error fetching CVE data: {str(e)}")
            break
    return []

def exa_search(query: SearchTerm) -> List[ExaData]:
    try:
        exa_client = Exa(api_key=EXA_API_KEY)
        results = exa_client.search(query.term)  
        return [ExaData(title=item['title'], url=item['url'], snippet=item['snippet']) for item in results.get('results', [])]
    except Exception as e:
        logger.error(f"Error fetching Exa.ai research: {str(e)}")
        return []

def duckduckgo_search(query: SearchTerm) -> List[DuckDuckGoResult]:
    try:
        tool = DuckDuckGoSearchRun()
        results = tool.run(query.term)
        return [DuckDuckGoResult(title=item['title'], url=item['url'], snippet=item['snippet']) for item in results]
    except Exception as e:
        if "Ratelimit" in str(e):
            logger.warning("DuckDuckGo search rate limit exceeded.")
        else:
            logger.error(f"Error fetching DuckDuckGo search results: {str(e)}")
        return []
