"""
Teams Bot UI - A comprehensive library for Microsoft Teams bot cards
"""

__version__ = "1.0.0"
__author__ = "Shubham Shinde"
__email__ = "your-email@example.com"

# Import main functions for easy access
from .cards.feedback_cards import create_feedback_card, create_feedback_detail_card
from .cards.response_cards import create_text_response_card, create_chart_response_card
from .cards.welcome_card import create_welcome_card, create_welcome_adaptive_card
from .cards.copilot_cards import create_bot_list_card, create_bot_detail_card
from .cards.session_cards import create_session_info_card
from .cards.chart_cards import create_chart_card
from .cards.carousel_cards import create_carousel_activity
from .cards.feature_cards import create_capabilities_card
from .cards.file_cards import create_file_analysis_card, create_file_preview_card

__all__ = [
    "create_feedback_card",
    "create_feedback_detail_card",
    "create_text_response_card",
    "create_chart_response_card",
    "create_welcome_card",
    "create_welcome_adaptive_card",
    "create_bot_list_card",
    "create_bot_detail_card",
    "create_session_info_card",
    "create_chart_card",
    "create_carousel_activity",
    "create_capabilities_card",
    "create_file_analysis_card",
    "create_file_preview_card",
]
