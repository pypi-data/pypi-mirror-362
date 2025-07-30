"""
Cards for collecting user feedback
"""

from botbuilder.schema import Attachment


def create_feedback_card(
    message_id: str,
    bot_code: str = None,
    session_id: str = None,
    query_id: str = None,
) -> Attachment:
    """
    Create a feedback card to append to responses

    Args:
        message_id (str): ID of the message to provide feedback on
        bot_code (str): The bot code for the feedback
        session_id (str): The session ID for the feedback
        query_id (str): The query ID for feedback tracking

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
                        "width": "stretch",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Was this response helpful?",
                                "wrap": True,
                                "size": "Small",
                            }
                        ],
                    },
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [
                            {
                                "type": "ActionSet",
                                "actions": [],
                            }
                        ],
                    },
                ],
            }
        ],
    }

    # Prepare data payloads
    positive_data = {
        "action": "feedback",
        "message_id": message_id,
        "is_positive": True,
    }

    negative_data = {
        "action": "feedback",
        "message_id": message_id,
        "is_positive": False,
    }

    # Add bot code and session ID if available
    if bot_code:
        positive_data["bot_code"] = bot_code
        negative_data["bot_code"] = bot_code

    if session_id:
        positive_data["session_id"] = session_id
        negative_data["session_id"] = session_id

    # Add query_id if available (defaulting to message_id if not provided)
    if query_id:
        positive_data["query_id"] = query_id
        negative_data["query_id"] = query_id

    # Set actions with updated data payloads
    card_json["body"][0]["columns"][1]["items"][0]["actions"] = [
        {
            "type": "Action.Submit",
            "title": "👍",
            "data": positive_data,
        },
        {
            "type": "Action.Submit",
            "title": "👎",
            "data": negative_data,
        },
    ]

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )


def create_feedback_detail_card(
    message_id: str,
    is_positive: bool,
    bot_code: str = None,
    session_id: str = None,
    query_id: str = None,
) -> Attachment:
    """
    Create a detailed feedback card when a user clicks thumbs up or down

    Args:
        message_id (str): ID of the message to provide feedback on
        is_positive (bool): Whether the initial feedback was positive
        bot_code (str): The bot code for the feedback
        session_id (str): The session ID for the feedback
        query_id (str): The query ID for feedback tracking

    Returns:
        Attachment: A card attachment
    """
    title = (
        "Thank you for your positive feedback!"
        if is_positive
        else "We're sorry this response wasn't helpful."
    )

    subtitle = (
        "What did you like about this response?"
        if is_positive
        else "Please tell us what went wrong:"
    )

    # Set different topic options based on feedback sentiment
    if is_positive:
        topic_choices = [
            {"title": "Answer accuracy", "value": "Answer accuracy"},
            {"title": "Helpful features", "value": "Helpful features"},
            {"title": "User experience", "value": "User experience"},
            {"title": "Response speed", "value": "Response speed"},
            {"title": "Other", "value": "Other"},
        ]
    else:
        topic_choices = [
            {"title": "Answer accuracy", "value": "Answer accuracy"},
            {"title": "Missing features", "value": "Missing Features"},
            {"title": "User experience", "value": "User experience"},
            {"title": "Response speed", "value": "Response speed"},
            {"title": "Other", "value": "Other"},
        ]

    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {"type": "TextBlock", "text": title, "size": "Medium", "weight": "Bolder"},
            {
                "type": "TextBlock",
                "text": subtitle,
                "wrap": True,
            },
            {
                "type": "Input.ChoiceSet",
                "id": "feedback_topics",
                "style": "expanded",
                "isMultiSelect": True,
                "value": "",
                "choices": topic_choices,
            },
            {
                "type": "Input.Text",
                "id": "feedback_description",
                "placeholder": "Additional details...",
                "isMultiline": True,
            },
        ],
    }

    # Store additional data fields as hidden inputs
    data_payload = {
        "action": "feedback_details",
        "message_id": message_id,
        "is_positive": is_positive,
    }

    # Add bot code and session ID if available
    if bot_code:
        data_payload["bot_code"] = bot_code

    if session_id:
        data_payload["session_id"] = session_id

    # Add query_id if available
    if query_id:
        data_payload["query_id"] = query_id

    # Add a submit button with the data payload
    card_json["body"].append(
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Submit",
                    "data": data_payload,
                }
            ],
        }
    )

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )
