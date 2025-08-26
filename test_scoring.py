from scoring import Scorer
from premiums import PREMIUMS

# Fake Board (not used directly in scorer)
class Board: 
    pass

class Move:
    def __init__(self, row, col, direction, word):
        self.row = row
        self.col = col
        self.direction = direction
        self.word = word.upper()

SCORES = {
    **dict.fromkeys("AEIOULNRST", 1),
    **dict.fromkeys("DG", 2),
    **dict.fromkeys("BCMP", 3),
    **dict.fromkeys("FHVWY", 4),
    "K": 5, "J": 8, "X": 8, "Q": 10, "Z": 10
}

def test_plain_word():
    move = Move(7, 0, 'H', 'DOG')
    assert Scorer(SCORES, {}).score_move(Board(), move) == 5  # 2+1+2

def test_with_premiums():
    move = Move(7, 7, 'H', 'DOG')  # D on TW, O on DL, G on TL
    # expected
