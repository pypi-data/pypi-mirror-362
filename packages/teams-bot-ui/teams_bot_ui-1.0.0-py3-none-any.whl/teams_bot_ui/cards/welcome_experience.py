from botbuilder.schema import Attachment
from typing import Optional, Dict, Any


def create_enhanced_welcome_card(
    user_name: Optional[str] = None, bot_info: Optional[Dict[str, Any]] = None
) -> Attachment:
    """
    Create an enhanced welcome card with visual appeal

    Args:
        user_name: Optional user name for personalization
        bot_info: Optional bot/assistant information (name, logo, etc.)

    Returns:
        Attachment: An adaptive card attachment
    """
    # Default bot info if not provided
    if not bot_info:
        bot_info = {
            "name": "Virtual Assistant",
            "logo": "https://via.placeholder.com/40?text=🤖",
        }

    # Personalized greeting
    greeting = (
        f"Welcome, {user_name}!"
        if user_name
        else f"Welcome to {bot_info.get('name', 'Virtual Assistant')}!"
    )

    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            # Header with logo and title
            {
                "type": "Container",
                "style": "emphasis",
                "bleed": True,
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
                                        "url": bot_info.get(
                                            "logo",
                                            "https://via.placeholder.com/40?text=🤖",
                                        ),
                                        "size": "Small",
                                        "style": "Person",
                                    }
                                ],
                                "verticalContentAlignment": "Center",
                            },
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": greeting,
                                        "size": "Medium",
                                        "weight": "Bolder",
                                        "wrap": True,
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Your AI assistant for questions and support",
                                        "isSubtle": True,
                                        "wrap": True,
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
            # What can I help with section
            {
                "type": "Container",
                "style": "default",
                "spacing": "Medium",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "✨ What would you like to do today?",
                        "weight": "Bolder",
                        "wrap": True,
                    }
                ],
            },
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "🔍 Ask a Question",
                "data": {
                    "action": "suggested_action",
                    "value": "I have a question",
                },
            },
            {
                "type": "Action.Submit",
                "title": "📚 Get Help",
                "data": {
                    "action": "suggested_action",
                    "value": "I need help with something",
                },
            },
            {
                "type": "Action.Submit",
                "title": "💡 Show Features",
                "data": {
                    "action": "suggested_action",
                    "value": "What can you do?",
                },
            },
        ],
    }

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )
