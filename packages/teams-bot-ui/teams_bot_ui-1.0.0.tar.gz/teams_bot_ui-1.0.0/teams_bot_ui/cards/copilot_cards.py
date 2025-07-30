"""
Cards for bot/assistant listing and selection
"""

from typing import List, Dict, Any
from botbuilder.schema import Attachment, CardAction, ActionTypes


def create_bot_list_card(bots: List[Dict[str, Any]]) -> Attachment:
    """
    Create a card showing available bots/assistants

    Args:
        bots (List[Dict]): List of bot info including id, name, description

    Returns:
        Attachment: A card attachment
    """
    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "size": "Medium",
                "weight": "Bolder",
                "text": "Available Assistants",
                "wrap": True,
                "style": "heading",
            },
            {
                "type": "TextBlock",
                "text": "Select an assistant to start a conversation:",
                "wrap": True,
            },
        ],
    }

    # Add a container for each bot
    items = []
    for bot in bots:
        item = {
            "type": "Container",
            "items": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [
                                {
                                    "type": "Image",
                                    "url": bot.get(
                                        "logo", "https://via.placeholder.com/32?text=🤖"
                                    ),
                                    "size": "Small",
                                    "style": "Person",
                                }
                            ],
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": bot.get("name", "Unknown"),
                                    "weight": "Bolder",
                                    "wrap": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "text": bot.get("description", ""),
                                    "spacing": "None",
                                    "wrap": True,
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "ActionSet",
                    "actions": [
                        {
                            "type": "Action.Submit",
                            "title": "Select",
                            "data": {
                                "action": "switch_bot",
                                "bot_code": bot.get("code", ""),
                            },
                        }
                    ],
                },
            ],
            "separator": True,
        }
        items.append(item)

    card_json["body"].extend(items)

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_bot_detail_card(bot: Dict[str, Any]) -> Attachment:
    """
    Create a card showing details of a specific bot/assistant

    Args:
        bot (Dict): Bot information

    Returns:
        Attachment: A card attachment
    """
    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [
                            {
                                "type": "Image",
                                "url": bot.get(
                                    "logo", "https://via.placeholder.com/64?text=🤖"
                                ),
                                "size": "Medium",
                            }
                        ],
                    },
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": bot.get("name", "Unknown Assistant"),
                                "size": "Medium",
                                "weight": "Bolder",
                                "wrap": True,
                            },
                            {
                                "type": "TextBlock",
                                "text": f"Code: {bot.get('code', 'Unknown')}",
                                "spacing": "Small",
                                "isSubtle": True,
                            },
                        ],
                    },
                ],
            },
            {"type": "TextBlock", "text": bot.get("description", ""), "wrap": True},
            {
                "type": "TextBlock",
                "text": "Capabilities:",
                "weight": "Bolder",
                "spacing": "Medium",
            },
        ],
    }

    # Add capabilities
    capabilities = bot.get("capabilities", [])
    for capability in capabilities:
        card_json["body"].append(
            {"type": "TextBlock", "text": f"• {capability}", "wrap": True}
        )

    # Add action buttons
    card_json["body"].append(
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Start Conversation",
                    "data": {
                        "action": "switch_bot",
                        "bot_code": bot.get("code", ""),
                    },
                },
                {
                    "type": "Action.OpenUrl",
                    "title": "Learn More",
                    "url": bot.get("link", "https://example.com"),
                },
            ],
        }
    )

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


# Backward compatibility aliases
def create_copilot_list_card(copilots: List[Dict[str, Any]]) -> Attachment:
    """
    Create a card showing available copilots (backward compatibility)

    Args:
        copilots (List[Dict]): List of copilot info including id, name, description

    Returns:
        Attachment: A card attachment
    """
    return create_bot_list_card(copilots)


def create_copilot_detail_card(copilot: Dict[str, Any]) -> Attachment:
    """
    Create a card showing details of a specific copilot (backward compatibility)

    Args:
        copilot (Dict): Copilot information

    Returns:
        Attachment: A card attachment
    """
    return create_bot_detail_card(copilot)
