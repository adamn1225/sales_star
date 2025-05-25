import re
from bs4 import BeautifulSoup
from typing import List

def extract_phone_numbers(text: str) -> List[str]:
    """
    Extracts valid phone numbers from the given text input.

    Args:
        text (str): The input text from which to extract phone numbers.

    Returns:
        List[str]: A list of valid phone numbers.
    """
    # Regular expression for valid phone numbers
    phone_pattern = re.compile(
        r'\+?\d{1,3}?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    )
    raw_numbers = phone_pattern.findall(text)

    # Filter out duplicates and invalid numbers
    valid_numbers = list(set(num for num in raw_numbers if len(re.sub(r'\D', '', num)) >= 7))
    return valid_numbers

def extract_tel_links(html: str) -> List[str]:
    """
    Extracts phone numbers from href="tel:" links in the given HTML.

    Args:
        html (str): The HTML content to parse.

    Returns:
        List[str]: A list of phone numbers from tel links.
    """
    soup = BeautifulSoup(html, "html.parser")
    tel_links = soup.find_all("a", href=True)
    phone_numbers = [link["href"].replace("tel:", "").strip() for link in tel_links if link["href"].startswith("tel:")]
    return phone_numbers