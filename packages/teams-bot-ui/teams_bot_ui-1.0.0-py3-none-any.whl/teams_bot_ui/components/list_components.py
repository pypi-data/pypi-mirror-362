"""
List components for Teams Adaptive Cards
"""

from typing import List, Dict, Any


def create_fact_set(facts: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Create a fact set for Adaptive Cards

    Args:
        facts (List[Dict]): List of facts with title and value keys

    Returns:
        Dict: A fact set object for Adaptive Cards
    """
    return {"type": "FactSet", "facts": facts}


def create_bullet_list(items: List[str]) -> List[Dict[str, Any]]:
    """
    Create a bullet list for Adaptive Cards

    Args:
        items (List[str]): List of text items

    Returns:
        List[Dict]: A list of TextBlock objects for Adaptive Cards
    """
    text_blocks = []
    for item in items:
        text_blocks.append({"type": "TextBlock", "text": f"• {item}", "wrap": True})

    return text_blocks


def create_numbered_list(items: List[str]) -> List[Dict[str, Any]]:
    """
    Create a numbered list for Adaptive Cards

    Args:
        items (List[str]): List of text items

    Returns:
        List[Dict]: A list of TextBlock objects for Adaptive Cards
    """
    text_blocks = []
    for i, item in enumerate(items, 1):
        text_blocks.append({"type": "TextBlock", "text": f"{i}. {item}", "wrap": True})

    return text_blocks
