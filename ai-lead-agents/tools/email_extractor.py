from typing import List
import re

def extract_emails(text: str) -> List[str]:
    """
    Extracts email addresses from the given text input.

    Args:
        text (str): The input text from which to extract email addresses.

    Returns:
        List[str]: A list of extracted email addresses.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)