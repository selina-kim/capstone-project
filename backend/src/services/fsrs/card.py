"""
services.fsrs.card

Module that defines the Card class.

Ref: https://github.com/open-spaced-repetition/py-fsrs/blob/main/fsrs/card.py
"""

from uuid import uuid4
from datetime import datetime, timezone
from services.fsrs.learning_state import LearningState
from pydantic import BaseModel, Field
from typing import Optional


class Card(BaseModel):
    """
    Represents a single flashcard in a deck.

    Attributes:
        card_id: str            # The id of the card. Created using uuid4() which generates a 128-bit ID with low chance of collisions.
        learning_state: int     # The card's current learning state.
        step: int               # The card's current learning or relearning step or None if the card is in the Review state.
        stability: float        # A mesaure of how long the card will stay in memory. This is used for future scheduling.
        difficulty: float       # A measure of how difficult the card is to remember. This is used for future scheduling.
        due: datetime           # The date and time when the card is due next.
        last_review: datetime   # The date and time of the card's last review.

    Usage:
        To dict:    data = card.model_dump()
        From dict:  card = Card.model_validate(data)
        To JSON:    json_str = card.model_dump_json(indent=2)
        From JSON:  Card.model_validate_json(json_str)
    """
    card_id: str = Field(default_factory=lambda: str(uuid4()))
    learning_state: LearningState = LearningState.Learning
    step: Optional[int] = None
    stability: Optional[float] = None
    difficulty: Optional[float] = None
    due: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_review: Optional[datetime] = None

    def model_post_init(self, __context):
        if self.learning_state == LearningState.Learning and self.step is None:
            self.step = 0
        if self.due.tzinfo is not None:
            self.due = self.due.astimezone(timezone.utc)

    def __str__(self) -> str:
        return self.__repr__()



# Usage examples - TODO delete below later :>
card = Card()

print(card.card_id)         # auto-generated UUID
print(card.learning_state)  # Learning
print(card.step)            # 0
print(card.due)             # now (UTC)



# To dict
data = card.model_dump()
print(data)

# From dict
card = Card.model_validate(data)
print(card)

# To JSON
json_str = card.model_dump_json(indent=2)
print(json_str)

# From JSON
print(Card.model_validate_json(json_str))