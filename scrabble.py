from typing import List, Optional
import random

class Move:
    def __init__(self, row: int, col: int, direction: str, word: str):
        self.row = row
        self.col = col
        self.direction = direction.upper()
        self.word = word.upper()

class Cell:
    def __init__(self, letter: Optional[str] = None, premium: Optional[str] = None):
        self.letter = letter
        self.premium = premium
        self.used_premium = False

class Bag:
    def __init__(self):
        self.tiles: List[str] = []

    def draw(self, n: int) -> List[str]:
        drawn = []
        for _ in range(min(n, len(self.tiles))):
            idx = random.randrange(len(self.tiles))
            drawn.append(self.tiles.pop(idx))
        return drawn

    def put_back(self, letters: List[str]):
        self.tiles.extend(letters)

    def __len__(self):
        return len(self.tiles)

class Board:
    def __init__(self, size: int = 15):
        self.size = size
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(size)] for _ in range(size)
        ]

    def get(self, r: int, c: int) -> Cell:
        return self.grid[r][c]

    def set(self, r: int, c: int, letter: str):
        self.grid[r][c].letter = letter

    def render(self) -> str:
        lines = []
        for row in self.grid:
            line = " ".join(cell.letter if cell.letter else "." for cell in row)
            lines.append(line)
        return "\n".join(lines)

class Player:
    def __init__(self, name: str, bag: Bag):
        self.name = name
        self.rack: List[str] = bag.draw(7)
        self.score = 0

    def refill(self, bag: Bag):
        needed = 7 - len(self.rack)
        self.rack.extend(bag.draw(needed))

    def has_letters(self, word_letters: List[str]) -> bool:
        temp_rack = self.rack.copy()
        for letter in word_letters:
            if letter in temp_rack:
                temp_rack.remove(letter)
            else:
                return False
        return True

    def consume_letters(self, used: List[str]):
        for letter in used:
            if letter in self.rack:
                self.rack.remove(letter)