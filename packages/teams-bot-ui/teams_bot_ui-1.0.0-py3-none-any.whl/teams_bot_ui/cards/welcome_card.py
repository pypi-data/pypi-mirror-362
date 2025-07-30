"""
Welcome card for first-time users
"""

from teams_bot_ui.cards.welcome_experience import create_enhanced_welcome_card
from typing import Optional, Dict, Any
from botbuilder.schema import (
    Attachment,
    HeroCard,
    CardAction,
    ActionTypes,
)


def create_welcome_card(user_name: str = None) -> Attachment:
    """
    Create a welcome card for first-time users

    Args:
        user_name (str): Optional user name for personalization

    Returns:
        Attachment: A Teams card attachment
    """
    greeting = (
        f"Welcome, {user_name}!" if user_name else "Welcome to Virtual Assistant!"
    )
    card = HeroCard(
        title=greeting,
        text="I'm your virtual assistant. Let me help you connect with the right bot.",
        images=[
            {
                "url": "https://via.placeholder.com/200x100?text=🤖+Virtual+Assistant",
            }
        ],
        buttons=[
            CardAction(
                type=ActionTypes.im_back,
                title="Select an Assistant",
                value="/assistants",
            ),
            CardAction(
                type=ActionTypes.im_back,
                title="Help",
                value="/help",
            ),
        ],
    )

    return Attachment(
        content_type="application/vnd.microsoft.card.hero",
        content=card,
    )


def create_welcome_adaptive_card(
    user_name: str = None,
    agent_code: Optional[str] = None,
    capabilities_text: Optional[str] = None,
    bot_info: Optional[Dict[str, Any]] = None,
) -> Attachment:
    """
    Create a welcome card using Adaptive Cards

    Args:
        user_name: Optional user name for personalization
        agent_code: Agent code if provided (determines button visibility)
        capabilities_text: Text describing bot capabilities
        bot_info: Optional bot/assistant information (name, logo, etc.)

    Returns:
        Attachment: An adaptive card attachment
    """
    greeting = f"Welcome, {user_name}!" if user_name else "Welcome!"

    # Basic card structure
    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "size": "Medium",
                "weight": "Bolder",
                "text": greeting,
                "horizontalAlignment": "Left",
                "wrap": True,
                "style": "heading",
            },
            {
                "type": "TextBlock",
                "text": "I'm your virtual assistant, ready to help you with your questions and tasks.",
                "wrap": True,
            },
        ],
    }

    # Add capabilities section if provided
    if capabilities_text and agent_code:
        # Clean capabilities text
        import re

        capabilities_text = re.sub(r'^text=["\'](.*?)["\']', r"\1", capabilities_text)
        capabilities_text = re.sub(
            r"image_url=.*$", "", capabilities_text, flags=re.DOTALL
        )
        capabilities_text = re.sub(
            r"query_id=.*$", "", capabilities_text, flags=re.DOTALL
        )

        bot_name = bot_info.get("name", "Assistant") if bot_info else "Assistant"

        card_json["body"].append(
            {
                "type": "Container",
                "style": "emphasis",
                "spacing": "Medium",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"**{bot_name} can help you with:**",
                        "wrap": True,
                        "weight": "Bolder",
                    },
                    {"type": "TextBlock", "text": capabilities_text, "wrap": True},
                ],
            }
        )

    # Only add buttons if no agent_code is provided
    if not agent_code:
        card_json["actions"] = [
            {
                "type": "Action.Submit",
                "title": "Select an Assistant",
                "data": {"action": "list_bots"},
            },
            {
                "type": "Action.Submit",
                "title": "Help",
                "data": {"action": "show_help"},
            },
        ]

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_enhanced_welcome_adaptive_card(
    user_name: str = None, bot_info: Optional[Dict[str, Any]] = None
) -> Attachment:
    """
    Create a visually enhanced welcome card using Adaptive Cards

    Args:
        user_name: Optional user name for personalization
        bot_info: Optional bot/assistant information (name, logo, etc.)

    Returns:
        Attachment: An adaptive card attachment
    """
    return create_enhanced_welcome_card(user_name, bot_info)


# Backward compatibility aliases
def create_copilot_welcome_card(user_name: str = None) -> Attachment:
    """
    Create a welcome card for first-time users (backward compatibility)

    Args:
        user_name (str): Optional user name for personalization

    Returns:
        Attachment: A Teams card attachment
    """
    return create_welcome_card(user_name)


def create_copilot_welcome_adaptive_card(
    user_name: str = None,
    agent_code: Optional[str] = None,
    capabilities_text: Optional[str] = None,
    copilot_info: Optional[Dict[str, Any]] = None,
) -> Attachment:
    """
    Create a welcome card using Adaptive Cards (backward compatibility)

    Args:
        user_name: Optional user name for personalization
        agent_code: Agent code if provided (determines button visibility)
        capabilities_text: Text describing copilot capabilities
        copilot_info: Optional copilot information (name, logo, etc.)

    Returns:
        Attachment: An adaptive card attachment
    """
    return create_welcome_adaptive_card(
        user_name, agent_code, capabilities_text, copilot_info
    )
