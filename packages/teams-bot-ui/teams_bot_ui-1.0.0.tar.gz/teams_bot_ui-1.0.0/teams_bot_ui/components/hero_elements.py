"""
Hero card elements for Teams bots
"""

from typing import List, Dict, Any
from botbuilder.schema import CardImage, CardAction, Attachment, HeroCard


def create_hero_card(
    title: str,
    text: str,
    buttons: List[CardAction] = None,
    images: List[CardImage] = None,
) -> Attachment:
    """
    Create a hero card

    Args:
        title (str): Card title
        text (str): Card text content
        buttons (List[CardAction]): Buttons to include
        images (List[CardImage]): Images to include

    Returns:
        Attachment: A hero card attachment
    """
    card = HeroCard(title=title, text=text, buttons=buttons, images=images)

    return Attachment(content_type="application/vnd.microsoft.card.hero", content=card)


def create_hero_image(url: str, alt: str = None) -> CardImage:
    """
    Create an image for a hero card

    Args:
        url (str): Image URL
        alt (str): Alt text

    Returns:
        CardImage: Image object for hero cards
    """
    return CardImage(url=url, alt=alt)
