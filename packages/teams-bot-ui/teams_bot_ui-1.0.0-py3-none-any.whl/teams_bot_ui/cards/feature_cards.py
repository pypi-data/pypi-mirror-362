from botbuilder.schema import Attachment
from typing import Optional, Dict, Any, List


def create_capabilities_card(
    bot_info: Optional[Dict[str, Any]] = None,
    features: Optional[List[Dict[str, str]]] = None,
) -> Attachment:
    """
    Create a visually appealing capabilities showcase card

    Args:
        bot_info: Optional bot information (name, logo, etc.)
        features: Optional list of features to showcase

    Returns:
        Attachment: An adaptive card attachment
    """
    # Default bot info if not provided
    if not bot_info:
        bot_info = {
            "name": "Virtual Assistant",
            "logo": "https://via.placeholder.com/40?text=🤖",
        }

    # Default features if not provided
    if not features:
        features = [
            {
                "title": "Answer Questions",
                "description": "Get detailed information about topics and answer your questions",
                "icon": "https://via.placeholder.com/40?text=❓",
            },
            {
                "title": "Find Information",
                "description": "Locate and summarize relevant information quickly",
                "icon": "https://via.placeholder.com/40?text=🔍",
            },
            {
                "title": "Provide Guidance",
                "description": "Get step-by-step guidance for various tasks and processes",
                "icon": "https://via.placeholder.com/40?text=📋",
            },
        ]

    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            # Header
            {
                "type": "Container",
                "style": "emphasis",
                "bleed": True,
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"Here's What {bot_info.get('name', 'I')} Can Help You With",
                        "size": "Large",
                        "weight": "Bolder",
                        "horizontalAlignment": "Center",
                        "wrap": True,
                    }
                ],
            }
        ],
    }

    # Add each feature
    for i, feature in enumerate(features):
        feature_container = {
            "type": "Container",
            "style": "default",
            "spacing": "Medium",
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
                                    "url": feature.get(
                                        "icon",
                                        f"https://via.placeholder.com/40?text={i+1}",
                                    ),
                                    "size": "Small",
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
                                    "text": feature.get("title", f"Feature {i+1}"),
                                    "weight": "Bolder",
                                    "wrap": True,
                                },
                                {
                                    "type": "TextBlock",
                                    "text": feature.get("description", ""),
                                    "isSubtle": True,
                                    "wrap": True,
                                },
                            ],
                        },
                    ],
                }
            ],
        }
        card_json["body"].append(feature_container)

    # Add action button
    card_json["actions"] = [
        {
            "type": "Action.Submit",
            "title": "Get Started",
            "data": {
                "action": "suggested_action",
                "value": "What can you help me with?",
            },
        }
    ]

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )
