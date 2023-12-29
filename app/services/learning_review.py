from datetime import datetime, timedelta
from app.enum import CardStageEnum, ReviewAnswerEnum

class LearningReviewService:
    @staticmethod
    def make_review(card, card_answer):
        learning_step = LearningReviewService.resolve_learning_step(card, card_answer)['learning_step']
        card.learning_step = learning_step
        due = LearningReviewService.learning_step_due_date(card)['due']
        if due:
            card.due = due
            return card

        graduating_card = LearningReviewService.graduating_card(card)
        card.stage = graduating_card['stage']
        card.learning_step = graduating_card['learning_step']
        card.current_interval = graduating_card['current_interval']
        card.due = graduating_card['due']
        return card

    @staticmethod
    def resolve_learning_step(card, card_answer):
        if card_answer in [ReviewAnswerEnum.AGAIN, ReviewAnswerEnum.HARD]:
            learning_step_decrement = card.learning_step - 1 if card.learning_step else 0
            return {'learning_step': learning_step_decrement}
        elif card_answer in [ReviewAnswerEnum.EASY, ReviewAnswerEnum.GOOD]:
            learning_step_increment = card.learning_step + 1
            return {'learning_step': learning_step_increment}

    @staticmethod
    def learning_step_due_date(card):
        learning_steps = card.deck.learning_steps

        current_learning_step = learning_steps[card.learning_step - 1] if card.learning_step <= len(learning_steps) else None

        if current_learning_step:
            due = datetime.now() + timedelta(seconds=current_learning_step.interval_time.total_seconds())

            return {'due': due}
        return {'due': None}

    @staticmethod
    def graduating_card(card):
        learning_steps = card.deck.learning_steps

        interval_last_learning_step = learning_steps[-1].interval_time if learning_steps else None

        current_interval = (
            round(interval_last_learning_step.total_seconds() / (60 * 60 * 24))
            if interval_last_learning_step
            else 1
        )

        due = datetime.now() + timedelta(days=card.current_interval)
        return {
            'stage': CardStageEnum.GRADUATED,
            'learning_step': 0,
            'current_interval': current_interval,
            'due': due,
        }
