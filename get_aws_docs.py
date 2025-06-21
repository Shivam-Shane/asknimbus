import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random
from files import links
from logger import logger

headers = {
    'User-Agent': 'AWSRAGBot/1.0 (Contact: data.console.store@gmail.com)'
}

# Reusable session with retry logic
session = requests.Session()
retries = requests.adapters.Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = requests.adapters.HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)

def save_failed_html(url, html):
    filename = f"failed_pages/{url.split('/')[-1]}.html"
    os.makedirs("failed_pages", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"Saved HTML snapshot to {filename}")

def scrape_aws_docs_single_page(url):
    try:
        logger.info(f"Getting Docs for {url}")
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        main_content = soup.find('div', id='main-col-body')
        if not main_content:
            logger.info(f"Main content div not found for {url}")
            save_failed_html(url, response.text)
            return ""

        text_parts = []
        for element in main_content.find_all(['h1', 'h2', 'h3', 'p']):
            text = element.get_text(strip=True)
            if text and len(text) > 20 and not text.startswith(('Sign in', 'Feedback')):
                text_parts.append(text)

        return " ".join(text_parts) if text_parts else ""
    except requests.RequestException as e:
        logger.error(f"Error fetching docs for {url}: {e}")
        return ""

def scrape_aws_KC_data(url):
    try:
        logger.info(f"Scraping KC data for {url}")
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        text_parts = []

        # Flexible title class
        title_div = soup.find('div', class_=lambda x: x and 'KCArticleView_title' in x)
        if title_div:
            h1_tag = title_div.find('h1')
            if h1_tag:
                text_parts.append(h1_tag.get_text(strip=True))
            else:
                logger.info(f"H1 tag not found in title div for {url}")
        else:
            logger.info(f"Title div not found for {url}")

        main_content = soup.find('div', class_='custom-md-style', attrs={'data-test': 'kcArticle-body'})
        if not main_content:
            logger.info(f"Main content div not found for {url}")
            save_failed_html(url, response.text)
            return ""

        for element in main_content.find_all(['h1', 'h2', 'h3', 'p', 'li', 'ul', 'ol']):
            text = element.get_text(strip=True)
            if text and len(text) > 20 and not text.startswith(('Sign in', 'Feedback')):
                text_parts.append(text)

        if not text_parts:
            logger.info(f"No useful text found in {url}")
            save_failed_html(url, response.text)

        return " ".join(text_parts) if text_parts else ""

    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return ""

def save_to_json(text, services, url):
    folder = "awsdocsdata"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, services + ".json")

    try:
        existing_data = {"data": "", "url": "", "metadata": ""}
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

        if text:
            existing_data["data"] += (" " + text) if existing_data["data"] else text

        existing_data["url"] = url
        existing_data["metadata"] = services

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        logger.info(f"Appended text to {filename} (total length: {len(existing_data['data'])} characters)")
    except Exception as e:
        logger.error(f"Error saving to JSON: {e}")

def extract_aws_knowledge_center_data_links(url):
    response = session.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("div", class_="PageDataView_col__p9XFi")
    new_links = []

    for idx, article in enumerate(articles, start=1):
        title_tag = article.find("a", class_="KCArticleCard_cardLink__EVTdA")
        if title_tag:
            link = title_tag.get("href")
            full_link = "https://repost.aws" + link if link.startswith("/") else link
            new_links.append(full_link)
        else:
            logger.info(f"{idx}. No title link found.")

    existing_links = []
    if os.path.exists("aws_KC_links.json"):
        with open("aws_KC_links.json", "r", encoding="utf-8") as f:
            existing_links = json.load(f)

    combined_links = list(set(existing_links + new_links))

    with open("aws_KC_links.json", "w", encoding="utf-8") as f:
        json.dump(combined_links, f, indent=2)

    logger.info(f"Added {len(new_links)} new links (total {len(combined_links)} links) to aws_KC_links.json")

if __name__ == "__main__":

    main_links=[
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiUjVKVmU1cml6Qno5bzFtb1ltUTRudz09IiwidCI6ImNHWjB1UlhNZnA0c2Q1OVJ4M01CZ3c9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiRUNkUjRBUG10RU14ZzY5Unl3WU1FZz09IiwidCI6Imo1Wml6NlAxN1UvemFESUllVVQ1M0E9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiWndSQUlaUUVZY24yeVozVlpSZEFoZz09IiwidCI6InpVZGlOUkU0RUs5ekR5dnd4ek5KbHc9PSJ9&pageSize=90"
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiK3JuQkQvb0xYamtHK0xBejBuQUhBQT09IiwidCI6Im8vL1h0cGNZV1dLampYdU1aZzUvK1E9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiYk5DbzlqNUtmaVNrQUpiakNsS2lwQT09IiwidCI6IjZ6WEkrcm92WjdwVXJTbTh5S0k3ZXc9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiSllmSDlla05hdWN2Tlh1OWVkWWtlUT09IiwidCI6ImRscnVQNVZZM1owcFM0TllsWitrQkE9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiVmhBSmdYbE1ENUt1d3RYOW1XcXV2dz09IiwidCI6IlJEZ2ZqUS85S1c4UkZlS2FNY2VRNFE9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiRVczeStMR0tWOXhlUlAxYjBHcU54dz09IiwidCI6IkxSbjdDZGozK2R2UlF4RkRhZ3hGeHc9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiM0JBM3VVNjBYYW5mTTZVOTFRM3JMdz09IiwidCI6IjdweUVCZ2N1eE1KQWxaa0xhNVBsS0E9PSJ9&pageSize=90",
        "https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiblhxU1FOcGhYbXpmNVRoWU9FQ3hoUT09IiwidCI6IjdNODVESEJBZDcxR2wxTzVQVC9kY3c9PSJ9&pageSize=90"
        
    ]
    for i in range(len(main_links)):
        extract_aws_knowledge_center_data_links(
        url=main_links[i])

    with open("aws_KC_links.json", "r", encoding="utf-8") as f:
        aws_KC_links = json.load(f)

    for link in aws_KC_links:
        scraped_text = scrape_aws_KC_data(link)
        if scraped_text:
            save_to_json(scraped_text, services="KC", url=link)
        time.sleep(random.uniform(1.0, 2.5))  # Respectful scraping delay

    for services,link in links.items():
        for i in range(len(link)):
            scraped_text = scrape_aws_docs_single_page(link[i])
            if scraped_text:
                save_to_json(scraped_text, services,link[i])
