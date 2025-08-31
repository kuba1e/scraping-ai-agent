import datetime
from typing import Union

from bs4 import BeautifulSoup
from httpx import Client
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.settings import ModelSettings

from core.load_models import OPEN_AI_MODEL
from schemas.product import ScrapingResult, Product

web_scraping_agent = Agent(
    name='Web Scraping Agent',
    model=OPEN_AI_MODEL,
    system_prompt=('''
        Your task is to convert a data string into a List of dictionaries.
        
        Step 1. Fetch the HTML text from the given URL using the fetch_html_text() function.
        Step 2. Takes the output from Step 1 and clean it up for the final output. 
    '''),
    retries=0,
    output_type=ScrapingResult,
    model_settings=ModelSettings(max_tokens=8000, temperature=0.1)
)

@web_scraping_agent.tool_plain(retries=1)
def fetch_html_text(url: str)->str:
    """
    Fetches an HTML text from given URL.

    :param url: The page URL to fetch HTML text from.
    :return: The HTML text from the given URL.
    """
    print(f"Calling URL: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    with Client(headers=headers) as client:
        response = client.get(url, timeout=20)
        print(response.text)
        if response.status_code != 200:
            return f'Failed to fetch the HTML text from {url}. Status code: {response.status_code}'

        soup = BeautifulSoup(response.text, 'html.parser')
        with open('soup.txt', 'w', encoding='utf-8') as f:
            f.write(soup.get_text())

        print('Soup file saved')

        return  soup.get_text().replace('\n', '').replace('\r', '')


@web_scraping_agent.tool_plain(retries=1)
def validate_result(result: ScrapingResult)->Union[ScrapingResult, None]:
    print('Start validating results')

    if isinstance(result, ScrapingResult):
        print('Validation passed')
        return result
    print('Validation failed')
    return None


def scrape_products_from_page_url(url:str)->list[Product] | None:
    try:
        response = web_scraping_agent.run_sync(url)
        if response.output.dataset is None:
            raise UnexpectedModelBehavior(message='No data returned from the model')

        print('-' * 50)
        print('Input tokens:', response.usage().input_tokens)
        print('Output tokens', response.usage().output_tokens)
        print('Total tokens', response.usage().total_tokens)

        products: list[Product] = []

        for item in response.output.dataset:
            product = item.model_dump()
            products.append(product)

        return products

    except UnexpectedModelBehavior as e:
        print(e)