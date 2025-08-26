# scoring.py

class Scorer:
    def __init__(self, letter_scores, premium_map):
        self.scores = letter_scores
        self.premiums = premium_map

    def score_move(self, board, move):
        r, c = move.row, move.col
        dr, dc = (0, 1) if move.direction == 'H' else (1, 0)
        word_mult, score = 1, 0

        for ch in move.word:
            letter_score = self.scores.get(ch, 0)
            prem = self.premiums.get((r, c))
            if prem == 'DL': letter_score *= 2
            if prem == 'TL': letter_score *= 3
            if prem == 'DW': word_mult *= 2
            if prem == 'TW': word_mult *= 3
            score += letter_score
            r += dr
            c += dc

        if len(move.word) == 7:
            score += 50  # bingo

        return score * word_mult
