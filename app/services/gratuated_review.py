from app.enum import ReviewAnswerEnum
from datetime import datetime, timedelta
from math import ceil


class GraduatedReviewService:
    @staticmethod
    def make_review(card, card_answer):
        card.ease = GraduatedReviewService.calculate_card_ease(card, card_answer)
        card.current_interval = GraduatedReviewService.calculate_card_interval(card, card_answer)
        card.due = (datetime.now() + timedelta(days=card.current_interval)).date()
        return card

    @staticmethod
    def calculate_card_ease(card, card_answer):
        if card_answer == ReviewAnswerEnum.AGAIN:
            return card.ease - 0.2 * card.ease
        elif card_answer == ReviewAnswerEnum.EASY:
            return card.ease + 0.15 * card.ease
        elif card_answer == ReviewAnswerEnum.GOOD:
            return card.ease
        elif card_answer == ReviewAnswerEnum.HARD:
            return card.ease - 0.15 * card.ease

    @staticmethod
    def calculate_card_interval(card, card_answer):
        if card_answer == ReviewAnswerEnum.AGAIN:
            return GraduatedReviewService.mark_card_as_again(card)
        elif card_answer == ReviewAnswerEnum.EASY:
            return GraduatedReviewService.mark_card_as_easy(card)
        elif card_answer == ReviewAnswerEnum.GOOD:
            return GraduatedReviewService.mark_card_as_good(card)
        elif card_answer == ReviewAnswerEnum.HARD:
            return GraduatedReviewService.mark_card_as_hard(card)

    @staticmethod
    def mark_card_as_good(card):
        return ceil(card.current_interval * card.ease * card.deck.interval_modifier)

    @staticmethod
    def mark_card_as_again(card):
        return ceil(card.current_interval - 0.5 * card.current_interval)

    @staticmethod
    def mark_card_as_hard(card):
        return ceil(card.current_interval * 1.2 * card.deck.interval_modifier)

    @staticmethod
    def mark_card_as_easy(card):
        return ceil(card.current_interval * card.ease * card.deck.interval_modifier * card.deck.easy_bonus)
