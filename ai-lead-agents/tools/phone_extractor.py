import re
from bs4 import BeautifulSoup
from typing import List

def extract_phone_numbers(html: str) -> List[str]:
    """
    Extracts phone numbers from both visible text and tel: links in the given HTML.
    Filters out numbers with 13+ digits and no formatting.
    """
    soup = BeautifulSoup(html, "html.parser")
    tel_links = soup.find_all("a", href=True)
    tel_numbers = [link["href"].replace("tel:", "").strip() for link in tel_links if link["href"].startswith("tel:")]

    # Regex for US and similar phone numbers (matches 712-792-9294, 712.792.9294, 712 792 9294, etc.)
    phone_pattern = re.compile(r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b')
    text_content = soup.get_text(separator=" ", strip=True)
    raw_numbers = phone_pattern.findall(text_content)
    print("=== PAGE TEXT ===")
    print(text_content)
    print("=== RAW NUMBERS ===")
    print(raw_numbers)
    all_numbers = tel_numbers + raw_numbers
    cleaned = []
    for num in all_numbers:
        digits = re.sub(r'\D', '', num)
        # Filter: skip if 13+ digits and no dashes, spaces, or parentheses
        if len(digits) >= 13 and not re.search(r'[-\s()]', num):
            continue
        if len(digits) == 10:
            cleaned.append(f"({digits[:3]}) {digits[3:6]}-{digits[6:]}")
        elif len(digits) == 11 and digits.startswith('1'):
            cleaned.append(f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}")
        elif 7 <= len(digits) < 13:
            cleaned.append(num.strip())
    return list(sorted(set(cleaned)))

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