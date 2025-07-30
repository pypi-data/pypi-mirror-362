"""
Reusable card templates for Teams bots
"""

from typing import Dict, Any, List, Optional
from botbuilder.schema import Attachment


def base_adaptive_card() -> Dict[str, Any]:
    """
    Get the base structure for an Adaptive Card

    Returns:
        Dict: Base Adaptive Card structure
    """
    return {"type": "AdaptiveCard", "version": "1.3", "body": []}


def add_text_block(
    card: Dict[str, Any],
    text: str,
    is_heading: bool = False,
    is_subtle: bool = False,
    wrap: bool = True,
) -> Dict[str, Any]:
    """
    Add a text block to an Adaptive Card

    Args:
        card (Dict): The card to modify
        text (str): Text content
        is_heading (bool): Whether this is a heading
        is_subtle (bool): Whether to use subtle styling
        wrap (bool): Whether to wrap text

    Returns:
        Dict: The modified card
    """
    text_block = {"type": "TextBlock", "text": text, "wrap": wrap}

    if is_heading:
        text_block.update({"size": "Medium", "weight": "Bolder"})

    if is_subtle:
        text_block["isSubtle"] = True

    card["body"].append(text_block)
    return card


def add_image(
    card: Dict[str, Any], url: str, size: str = "Medium", alt_text: str = None
) -> Dict[str, Any]:
    """
    Add an image to an Adaptive Card

    Args:
        card (Dict): The card to modify
        url (str): Image URL
        size (str): Image size (Small, Medium, Large)
        alt_text (str): Alternative text

    Returns:
        Dict: The modified card
    """
    image = {"type": "Image", "url": url, "size": size}

    if alt_text:
        image["altText"] = alt_text

    card["body"].append(image)
    return card


def add_action_set(
    card: Dict[str, Any], actions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Add an action set to an Adaptive Card

    Args:
        card (Dict): The card to modify
        actions (List[Dict]): List of actions

    Returns:
        Dict: The modified card
    """
    card["body"].append({"type": "ActionSet", "actions": actions})

    return card


def create_adaptive_attachment(card_json: Dict[str, Any]) -> Attachment:
    """
    Create an Attachment from an Adaptive Card JSON

    Args:
        card_json (Dict): The Adaptive Card JSON

    Returns:
        Attachment: A card attachment
    """
    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_container(
    elements: List[Dict[str, Any]], style: Optional[str] = None, separator: bool = False
) -> Dict[str, Any]:
    """
    Create a container for Adaptive Cards

    Args:
        elements (List[Dict]): List of elements to include
        style (str): Optional style (Default, Emphasis, Good, Warning, Attention)
        separator (bool): Whether to include a separator

    Returns:
        Dict: A container object
    """
    container = {"type": "Container", "items": elements, "separator": separator}

    if style:
        container["style"] = style

    return container
