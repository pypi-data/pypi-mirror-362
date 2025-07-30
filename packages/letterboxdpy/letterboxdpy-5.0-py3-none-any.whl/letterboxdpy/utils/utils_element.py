from typing import Optional

def get_text_if_exists(dom, tag: str, **kwargs) -> Optional[str]:
    """
    Get text from the DOM element matching the tag and criteria if exists. Returns None if not found.
    """
    elem = dom.find(tag, **kwargs)
    return elem.text.strip() if elem else None

def get_attribute_if_exists(dom, tag: str, attribute_name: str, **kwargs) -> Optional[str]:
    """
    Get attribute value from the DOM element matching the tag and criteria if exists. Returns None if not found.
    """
    elem = dom.find(tag, **kwargs)
    return elem[attribute_name] if elem and attribute_name in elem.attrs else None

def get_list_from_text(text: str, separator: str = ', ') -> list:
    """
    Split text into a list using the specified separator and trim whitespace if text exists. Returns an empty list if text is None.
    """
    return [i.strip() for i in text.split(separator)] if text else []

def extract_numeric_text(text: str) -> Optional[str]:
    """
    Extract numeric part from the text. Placeholder function.
    """
    # Placeholder implementation for extracting numeric text
    return ''.join(filter(str.isdigit, text)) if text else None