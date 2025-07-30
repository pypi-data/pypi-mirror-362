"""
Cards for formatted responses from the bot
"""

from teams_bot_ui.cards.chart_cards import create_chart_card
from typing import List, Optional, Dict, Any
from botbuilder.schema import Attachment


def create_text_response_card(
    response_text: str,
    bot_info: Optional[Dict[str, Any]] = None,
    suggested_actions: Optional[List[Dict[str, str]]] = None,
) -> Attachment:
    """
    Create a card for text responses

    Args:
        response_text (str): The response text
        bot_info (Dict): Information about the active bot/assistant
        suggested_actions (List): List of suggested follow-up actions

    Returns:
        Attachment: A card attachment
    """
    # Format the response text with markdown
    formatted_text = response_text

    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [{"type": "TextBlock", "text": formatted_text, "wrap": True}],
    }

    # Add bot info if provided
    if bot_info:
        header = {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": bot_info.get(
                                "logo", "https://via.placeholder.com/16?text=🤖"
                            ),
                            "size": "Small",
                        }
                    ],
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": bot_info.get("name", "AI Assistant"),
                            "size": "Small",
                            "weight": "Bolder",
                        }
                    ],
                },
            ],
        }
        card_json["body"].insert(0, header)

    # Add suggested actions if provided
    if suggested_actions and len(suggested_actions) > 0:
        actions = []
        for action in suggested_actions:
            actions.append(
                {
                    "type": "Action.Submit",
                    "title": action.get("title", "Action"),
                    "data": {
                        "action": "suggested_action",
                        "value": action.get("value", ""),
                    },
                }
            )

        card_json["body"].append(
            {
                "type": "TextBlock",
                "text": "Suggested follow-ups:",
                "size": "Small",
                "weight": "Bolder",
                "spacing": "Medium",
            }
        )

        card_json["body"].append({"type": "ActionSet", "actions": actions})

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_image_response_card(
    response_text: str, image_url: str, bot_info: Optional[Dict[str, Any]] = None
) -> Attachment:
    """
    Create a card for responses with images

    Args:
        response_text (str): The response text
        image_url (str): URL to the image
        bot_info (Dict): Information about the active bot/assistant

    Returns:
        Attachment: A card attachment
    """
    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {"type": "TextBlock", "text": response_text, "wrap": True},
            {"type": "Image", "url": image_url, "size": "Large"},
        ],
    }

    # Add bot info if provided
    if bot_info:
        header = {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": bot_info.get(
                                "logo", "https://via.placeholder.com/16?text=🤖"
                            ),
                            "size": "Small",
                        }
                    ],
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": bot_info.get("name", "AI Assistant"),
                            "size": "Small",
                            "weight": "Bolder",
                        }
                    ],
                },
            ],
        }
        card_json["body"].insert(0, header)

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_error_card(error_message: str) -> Attachment:
    """
    Create a card for error messages

    Args:
        error_message (str): The error message

    Returns:
        Attachment: A card attachment
    """
    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": "⚠️ Error",
                "size": "Medium",
                "weight": "Bolder",
                "color": "Attention",
            },
            {"type": "TextBlock", "text": error_message, "wrap": True},
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Try Again",
                        "data": {"action": "try_again"},
                    },
                    {
                        "type": "Action.Submit",
                        "title": "Help",
                        "data": {"action": "show_help"},
                    },
                ],
            },
        ],
    }

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_file_processing_card(
    filenames: List[str], bot_info: Optional[Dict[str, Any]] = None
) -> Attachment:
    """
    Create a card showing file processing status

    Args:
        filenames (List[str]): List of filenames being processed
        bot_info (Dict): Information about the active bot/assistant

    Returns:
        Attachment: A card attachment
    """
    if len(filenames) == 1:
        title = f"Processing file: {filenames[0]}"
    else:
        title = f"Processing {len(filenames)} files"

    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": title,
                "size": "Medium",
                "weight": "Bolder",
            },
            {
                "type": "TextBlock",
                "text": "Please wait while I analyze the content...",
                "wrap": True,
            },
        ],
    }

    # Add file list if multiple files
    if len(filenames) > 1:
        file_list = []
        for filename in filenames:
            file_list.append(
                {
                    "type": "TextBlock",
                    "text": f"• {filename}",
                    "wrap": True,
                }
            )

        card_json["body"].append({"type": "Container", "items": file_list})

    # Add bot info if provided
    if bot_info:
        header = {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": bot_info.get(
                                "logo", "https://via.placeholder.com/16?text=🤖"
                            ),
                            "size": "Small",
                        }
                    ],
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": bot_info.get("name", "AI Assistant"),
                            "size": "Small",
                            "weight": "Bolder",
                        }
                    ],
                },
            ],
        }
        card_json["body"].insert(0, header)

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_chart_response_card(
    chart_title: str,
    chart_data: Dict[str, Any],
    chart_type: str = "bar",
    response_text: Optional[str] = None,
    bot_info: Optional[Dict[str, Any]] = None,
) -> Attachment:
    """
    Create a response card with a chart visualization

    Args:
        chart_title: Title for the chart
        chart_data: Data for the chart visualization
        chart_type: Type of chart (bar, line, pie)
        response_text: Optional text to display above the chart
        bot_info: Information about the active bot/assistant

    Returns:
        Attachment: A card attachment
    """
    # If there's response text, create a text card first
    if response_text:
        text_card = create_text_response_card(
            response_text=response_text, bot_info=bot_info
        )

    # Create the chart card
    chart_card = create_chart_card(
        title=chart_title,
        chart_data=chart_data,
        chart_type=chart_type,
        copilot_info=bot_info,  # Chart card still uses copilot_info parameter for backward compatibility
    )

    # Return either just the chart card or both cards
    return chart_card


# Backward compatibility aliases
def create_copilot_response_card(
    response_text: str,
    copilot_info: Optional[Dict[str, Any]] = None,
    suggested_actions: Optional[List[Dict[str, str]]] = None,
) -> Attachment:
    """
    Create a card for text responses (backward compatibility)

    Args:
        response_text (str): The response text
        copilot_info (Dict): Information about the active copilot
        suggested_actions (List): List of suggested follow-up actions

    Returns:
        Attachment: A card attachment
    """
    return create_text_response_card(response_text, copilot_info, suggested_actions)
