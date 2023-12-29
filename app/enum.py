from enum import Enum

class CardStageEnum(Enum):
    LEARNING = 'LEARNING'
    GRADUATED = 'GRADUATED'
    # RELEARNING = 'RELEARNING'

class ReviewAnswerEnum(Enum):
    AGAIN = 'AGAIN'
    HARD = 'HARD'
    EASY = 'EASY'
    GOOD = 'GOOD'