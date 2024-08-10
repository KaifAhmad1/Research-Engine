# data/datafetching.py

import logging
import asyncio
import aiohttp
from typing import List, Dict, Any
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

# Asynchronous data collection functions
async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return {"url": url, "content": await response.text()}
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return None

async def scrape_websites(websites: List[Website]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, website.url) for website in websites]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

async def fetch_tweets(query: SearchTerm, max_tweets: int = 100) -> List[Tweet]:
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

async def fetch_cve_data() -> List[CVEData]:
    retries = 3
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://cve.circl.lu/api/last", timeout=30) as response:
                    response.raise_for_status()
                    return [CVEData(**item) for item in await response.json()]
        except aiohttp.ClientTimeout:
            logger.warning(f"Timeout error. Retrying ({attempt + 1}/{retries})...")
        except Exception as e:
            logger.error(f"Error fetching CVE data: {str(e)}")
            break
    return []

async def exa_search(query: SearchTerm) -> List[ExaData]:
    try:
        exa_client = Exa(api_key=EXA_API_KEY)
        results = exa_client.search(query.term)
        return [ExaData(title=item['title'], url=item['url'], snippet=item['snippet']) for item in results.get('results', [])]
    except Exception as e:
        logger.error(f"Error fetching Exa.ai research: {str(e)}")
        return []

async def duckduckgo_search(query: SearchTerm) -> List[DuckDuckGoResult]:
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

# Main data collection function
async def collect_data(input_data: InputData) -> OutputData:
    web_data, tweet_data, cve_data, exa_data, duckduckgo_data = await asyncio.gather(
        scrape_websites(input_data.websites),
        *[fetch_tweets(term, max_tweets=50) for term in input_data.search_terms],
        fetch_cve_data(),
        *[exa_search(term) for term in input_data.search_terms],
        *[duckduckgo_search(term) for term in input_data.search_terms]
    )

    tweet_data = [item for sublist in tweet_data for item in sublist]
    exa_data = [item for sublist in exa_data for item in sublist]
    duckduckgo_data = [item for sublist in duckduckgo_data for item in sublist]

    return OutputData(
        web_data=web_data,
        tweet_data=tweet_data,
        cve_data=cve_data,
        exa_data=exa_data,
        duckduckgo_data=duckduckgo_data,
    )

