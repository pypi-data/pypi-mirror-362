"""
Button components for Teams cards
"""

from botbuilder.schema import CardAction, ActionTypes
from typing import Dict, Any


def create_submit_button(title: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a submit button for an Adaptive Card

    Args:
        title (str): Button text
        data (Dict): Data to send when clicked

    Returns:
        Dict: Button object for Adaptive Card
    """
    return {"type": "Action.Submit", "title": title, "data": data}


def create_url_button(title: str, url: str) -> Dict[str, Any]:
    """
    Create a URL button for an Adaptive Card

    Args:
        title (str): Button text
        url (str): URL to open

    Returns:
        Dict: Button object for Adaptive Card
    """
    return {"type": "Action.OpenUrl", "title": title, "url": url}


def create_card_action(
    title: str, value: str, action_type: str = ActionTypes.im_back
) -> CardAction:
    """
    Create a card action for Hero Cards

    Args:
        title (str): Button text
        value (str): Value sent when clicked
        action_type (str): Type of action

    Returns:
        CardAction: A card action for Hero Cards
    """
    return CardAction(type=action_type, title=title, value=value)
