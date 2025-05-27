import requests
from bs4 import BeautifulSoup
import json
import os
from files import links
from logger import logger
headers = {
        'User-Agent': 'AWSRAGBot/1.0 (Contact: data.console.store@gmail.com)'
    }
def scrape_aws_docs_single_page(url):
    """
    Scrape text from the main content div of an AWS Documentation page.
    Returns a single string with all text and the URL.
    """
    headers = {
        'User-Agent': 'AWSRAGBot/1.0 (Contact: data.console.store@gmail.com)'
    }
    
    try:
        logger.info(f"Getting Docs for {url}")
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main content div
        main_content = soup.find('div', id='main-col-body')
        if not main_content:
            logger.info("Main content div not found.")
            return ""
        
        # Extract text from h1, h2, h3, and p tags
        text_parts = []
        for element in main_content.find_all(['h1', 'h2', 'h3', 'p']):
            text = element.get_text(strip=True)
            # Filter out short or irrelevant text
            if text and len(text) > 20 and not text.startswith(('Sign in', 'Feedback')):
                text_parts.append(text)
        
        # Concatenate text with spaces and add URL
        if text_parts:
            concatenated_text = " ".join(text_parts)
            return concatenated_text
        return ""
    
    except requests.RequestException as e:
        logger.error(f"Error fetching docs for {url}: {e}")
        return ""

def save_to_json(text,services,url):
    """
    Append or save scraped text to a single JSON file under the 'data' key.
    """
    folder="awsdocsdata"
    if not os.path.exists(folder):
        os.makedirs(folder,exist_ok=True)

    filename = os.path.join(folder,services+".json")
    try:
        # Load existing data if file exists
        existing_data = {"data": "","url":"","metadata":""}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            pass  # File doesn't exist yet
        
        # Append new text to the 'data' string
        if text:
            if existing_data["data"]:
                existing_data["data"] += " " + text  # Append with a space
            else:
                existing_data["data"] = text
        existing_data['url']=url
        existing_data['metadata']=services
        # Save to JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        logger.info(f"Appended text to {filename} (total length: {len(existing_data['data'])} characters)")
    except Exception as e:
        logger.error(f"Error saving to JSON: {e}")

def extract_aws_knowledge_center_data_links(url):
    """
    Fetch AWS Knowledge Center article links from a given URL and append them to a JSON file.
    """

    # Send GET request
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article containers
    articles = soup.find_all("div", class_="PageDataView_col__p9XFi")
    new_links = []

    for idx, article in enumerate(articles, start=1):
        title_tag = article.find("a", class_="KCArticleCard_cardLink__EVTdA")
        if title_tag:
            link = title_tag.get("href")
            full_link = "https://repost.aws" + link if link.startswith("/") else link
            new_links.append(full_link)
        else:
            print(f"{idx}. No title link found.")

    # Load existing links if file exists
    existing_links = []
    if os.path.exists("aws_KC_links.json"):
        with open("aws_KC_links.json", "r", encoding="utf-8") as f:
            existing_links = json.load(f)
    logger.info(existing_links)
    # Combine and deduplicate links
    combined_links = list(set(existing_links + new_links))

    # Save updated list
    with open("aws_KC_links.json", "w", encoding="utf-8") as f:
        json.dump(combined_links, f, indent=2)

    logger.info(f"Added {len(new_links)} new links (total {len(combined_links)} links) to aws_KC_links.json")

def scrape_aws_KC_data(url):
    """
    Scrape text from the main content div of an AWS Documentation page.
    Returns a single string with all text and the URL.
    """
    
    try:
        # Fetch the page
        text_parts = []
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Step 1: Extract the h1 tag from div with class 'KCArticleView_title___TWq1'
        title_div = soup.find('div', class_='KCArticleView_title___TWq1')
        title = ""
        if title_div:
            h1_tag = title_div.find('h1')
            if h1_tag:
                title = h1_tag.get_text(strip=True)
                # print("Title:", title)
                text_parts.append(title)
            else:
                logger.info("H1 tag not found within title div.")
        else:
            logger.info("Title div with class 'KCArticleView_title___TWq1' not found.")
        

        # Parse HTML with BeautifulSoup
        
        main_content = soup.find('div', class_='custom-md-style', attrs={'data-test': 'kcArticle-body'})
        if not main_content:
            logger.info("Main content div not found.")
            return ""

        # Extract text from h1, h2, h3, and p tags
        for element in main_content.find_all(['h1', 'h2', 'h3', 'p','li','ul','ol']):
            text = element.get_text(strip=True)
            # Filter out short or irrelevant text
            if text and len(text) > 20 and not text.startswith(('Sign in', 'Feedback')):
                text_parts.append(text)

        # Concatenate text with spaces and add URL
        if text_parts:
            concatenated_text = " ".join(text_parts)
            return concatenated_text

    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return ""

if __name__=="__main__":

    extract_aws_knowledge_center_data_links(url="https://repost.aws/knowledge-center/all?view=all&sort=recent&page=eyJ2IjoyLCJuIjoiMldrNDBJU2d6RGJldXN1SzB4VWVyUT09IiwidCI6Ino2MXJOOW9TOVFwb0V1Y1lpMFBRUFE9PSJ9&pageSize=90")

    for services,link in links.items():
        for i in range(len(link)):
            scraped_text = scrape_aws_docs_single_page(link[i])
            if scraped_text:
                save_to_json(scraped_text, services,link[i])

    with open("aws_KC_links.json","r", encoding="utf-8") as f:
        links=json.load(f)
    
    for link in links:
        scraped_text=scrape_aws_KC_data(link)
        if scraped_text:
            save_to_json(scraped_text,services="KC",url=link)