"""
Basic tests for teams-bot-ui package
"""

import pytest
from botbuilder.schema import Attachment


def test_package_import():
    """Test that the package can be imported"""
    import teams_bot_ui

    assert teams_bot_ui.__version__ is not None


def test_create_text_response_card():
    """Test creating a basic text response card"""
    from teams_bot_ui import create_text_response_card

    card = create_text_response_card("Hello World")

    assert isinstance(card, Attachment)
    assert card.content_type == "application/vnd.microsoft.card.adaptive"
    assert "Hello World" in str(card.content)


def test_create_welcome_card():
    """Test creating a welcome card"""
    from teams_bot_ui import create_welcome_card

    card = create_welcome_card("John")

    assert isinstance(card, Attachment)
    assert card.content_type == "application/vnd.microsoft.card.hero"


def test_create_feedback_card():
    """Test creating a feedback card"""
    from teams_bot_ui import create_feedback_card

    card = create_feedback_card("test_message_id")

    assert isinstance(card, Attachment)
    assert card.content_type == "application/vnd.microsoft.card.adaptive"


def test_create_chart_card():
    """Test creating a chart card"""
    from teams_bot_ui import create_chart_card

    chart_data = {
        "labels": ["A", "B", "C"],
        "datasets": [{"label": "Test Data", "data": [1, 2, 3]}],
    }

    card = create_chart_card("Test Chart", chart_data)

    assert isinstance(card, Attachment)
    assert card.content_type == "application/vnd.microsoft.card.adaptive"


def test_bot_info_parameter():
    """Test that bot_info parameter works correctly"""
    from teams_bot_ui import create_text_response_card

    bot_info = {"name": "Test Bot", "logo": "https://example.com/logo.png"}

    card = create_text_response_card(response_text="Test message", bot_info=bot_info)

    assert isinstance(card, Attachment)
    card_content = str(card.content)
    assert "Test Bot" in card_content


def test_suggested_actions():
    """Test that suggested actions work correctly"""
    from teams_bot_ui import create_text_response_card

    suggested_actions = [
        {"title": "Action 1", "value": "action1"},
        {"title": "Action 2", "value": "action2"},
    ]

    card = create_text_response_card(
        response_text="Choose an action:", suggested_actions=suggested_actions
    )

    assert isinstance(card, Attachment)
    card_content = str(card.content)
    assert "Action 1" in card_content
    assert "Action 2" in card_content


if __name__ == "__main__":
    pytest.main([__file__])
