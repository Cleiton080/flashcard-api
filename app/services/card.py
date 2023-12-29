from app.models import CardModel
from app.enum import CardStageEnum
from app.exceptions import CannotReviewCard
from app.services.learning_review import LearningReviewService
from app.services.gratuated_review import GraduatedReviewService
from app.services.review import ReviewService

class CardService:
    @staticmethod
    def process_review(card_id, card_answer):
        card = CardModel.find_by_id(card_id)

        if not ReviewService.can_review_card(card):
            raise CannotReviewCard()

        if card.stage is CardStageEnum.LEARNING:
            card = LearningReviewService.make_review(card, card_answer)

        if card.stage is CardStageEnum.GRADUATED:
            card = GraduatedReviewService.make_review(card, card_answer)

        # if card.card_stage is CardStageEnum.RELEARNING:
        #     pass

        card.save_to_db()
