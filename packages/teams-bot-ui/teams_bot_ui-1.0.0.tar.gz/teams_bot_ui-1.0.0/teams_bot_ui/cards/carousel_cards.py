from botbuilder.schema import (
    Activity,
    ActivityTypes,
    Attachment,
    CardAction,
    ActionTypes,
    HeroCard,
    AttachmentLayoutTypes,
)
from typing import List, Dict, Any


def create_carousel_activity(items: List[Dict[str, Any]]) -> Activity:
    """
    Create a carousel of cards

    Args:
        items: List of items to display in the carousel, each with 'title', 'subtitle', 'image', 'text', and 'buttons'

    Returns:
        Activity: A message activity with carousel attachment layout
    """
    # Create a hero card for each item
    attachments = []
    for item in items:
        # Prepare buttons
        buttons = []
        for button in item.get("buttons", []):
            action_type = ActionTypes.im_back
            if button.get("type") == "openUrl":
                action_type = ActionTypes.open_url

            buttons.append(
                CardAction(
                    type=action_type,
                    title=button.get("title", "View"),
                    value=button.get("value", ""),
                )
            )

        # Create hero card
        hero = HeroCard(
            title=item.get("title", ""),
            subtitle=item.get("subtitle", ""),
            text=item.get("text", ""),
            images=[{"url": item.get("image")}] if item.get("image") else None,
            buttons=buttons,
        )

        attachments.append(
            Attachment(content_type="application/vnd.microsoft.card.hero", content=hero)
        )

    # Create a reply activity with the carousel
    reply = Activity(
        type=ActivityTypes.message,
        attachments=attachments,
        attachment_layout=AttachmentLayoutTypes.carousel,
    )

    return reply
