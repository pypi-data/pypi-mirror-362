"""
Cards for displaying session information
"""

from typing import Dict, Any, Optional
from botbuilder.schema import Attachment


def create_session_info_card(
    bot_code: str,
    bot_name: str,
    session_id: str,
    message_count: Optional[int] = None,
    start_time: Optional[str] = None,
    logo_url: Optional[str] = None,
) -> Attachment:
    """
    Create a card showing session information

    Args:
        bot_code (str): Bot code (e.g., ABC-XYZ)
        bot_name (str): Friendly name of the bot/assistant
        session_id (str): Session identifier
        message_count (int): Number of messages in session
        start_time (str): Session start time
        logo_url (str): URL to bot logo

    Returns:
        Attachment: A card attachment
    """
    session_display = session_id

    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": "Active Assistant Session",
                "size": "Medium",
                "weight": "Bolder",
            },
            {
                "type": "FactSet",
                "facts": [
                    {"title": "Assistant:", "value": f"{bot_name} ({bot_code})"},
                    {"title": "Session ID:", "value": session_display},
                ],
            },
        ],
    }

    # Add optional info if provided
    facts = card_json["body"][1]["facts"]
    if message_count is not None:
        facts.append({"title": "Messages:", "value": str(message_count)})

    if start_time:
        facts.append({"title": "Started:", "value": start_time})

    # Add action buttons
    card_json["body"].append(
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Clear Conversation",
                    "data": {"action": "clear_session"},
                },
                {
                    "type": "Action.Submit",
                    "title": "Switch Assistant",
                    "data": {"action": "list_bots"},
                },
            ],
        }
    )

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_no_session_card() -> Attachment:
    """
    Create a card for when no active session exists

    Returns:
        Attachment: A card attachment
    """
    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": "No Active Session",
                "size": "Medium",
                "weight": "Bolder",
            },
            {
                "type": "TextBlock",
                "text": "You don't have an active assistant session. Please select an assistant to start a conversation.",
                "wrap": True,
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Select an Assistant",
                        "data": {"action": "list_bots"},
                    }
                ],
            },
        ],
    }

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


# Backward compatibility aliases
def create_copilot_session_info_card(
    copilot_code: str,
    copilot_name: str,
    session_id: str,
    message_count: Optional[int] = None,
    start_time: Optional[str] = None,
    logo_url: Optional[str] = None,
) -> Attachment:
    """
    Create a card showing session information (backward compatibility)

    Args:
        copilot_code (str): Copilot code (e.g., ABC-XYZ)
        copilot_name (str): Friendly name of the copilot
        session_id (str): Session identifier
        message_count (int): Number of messages in session
        start_time (str): Session start time
        logo_url (str): URL to copilot logo

    Returns:
        Attachment: A card attachment
    """
    return create_session_info_card(
        copilot_code, copilot_name, session_id, message_count, start_time, logo_url
    )
