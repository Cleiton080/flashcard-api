from datetime import datetime


class ReviewService:
    @classmethod
    def can_review_card(cls, card):
        if card.due is None:
            return True

        current_time = datetime.now().timestamp()
        card_due = card.due.timestamp()

        return card_due <= current_time