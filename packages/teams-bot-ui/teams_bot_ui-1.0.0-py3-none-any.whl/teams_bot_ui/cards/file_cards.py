"""
Cards for displaying file analysis results
"""

from typing import List, Dict, Any, Optional
from botbuilder.schema import Attachment


def create_file_analysis_card(
    processing_results: List[Any], bot_info: Optional[Dict[str, Any]] = None
) -> Attachment:
    """
    Create a card showing file analysis results

    Args:
        processing_results: The file processing results
        bot_info: Information about the active bot/assistant

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
                "text": f"File Analysis ({len(processing_results)} files)",
                "wrap": True,
            }
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

    # Add file content
    for result in processing_results:
        if result.success:
            container = {
                "type": "Container",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": result.file_info.name,
                        "weight": "Bolder",
                        "wrap": True,
                    },
                    {
                        "type": "TextBlock",
                        "text": result.summary,
                        "wrap": True,
                        "size": "Small",
                    },
                ],
                "separator": True,
            }

            if result.highlights:
                highlights = " • ".join(result.highlights)
                container["items"].append(
                    {
                        "type": "TextBlock",
                        "text": f"Highlights: {highlights}",
                        "wrap": True,
                        "size": "Small",
                        "isSubtle": True,
                    }
                )

            card_json["body"].append(container)

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_file_preview_card(
    file_info: Dict[str, Any],
    content_preview: str,
    bot_info: Optional[Dict[str, Any]] = None,
) -> Attachment:
    """
    Create a card showing a preview of file content

    Args:
        file_info: File information
        content_preview: Text preview of the content
        bot_info: Information about the active bot/assistant

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
                "text": f"File Preview: {file_info.get('name', 'Unknown')}",
                "wrap": True,
            },
            {
                "type": "TextBlock",
                "text": f"Type: {file_info.get('content_type', 'Unknown')}",
                "wrap": True,
                "size": "Small",
                "isSubtle": True,
            },
            {
                "type": "Container",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": content_preview,
                        "wrap": True,
                        "size": "Small",
                    }
                ],
            },
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
