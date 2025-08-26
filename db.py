import sqlite3
from typing import List

DB_FILE = "scrabble.db"

class DB:
    def __init__(self, db_file: str = DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.init_schema()

    def init_schema(self):
        self.cur.executescript("""
        PRAGMA journal_mode=WAL;

        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            total_score INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player1 TEXT NOT NULL,
            player2 TEXT NOT NULL,
            board_state TEXT,
            racks_state TEXT,
            bag_state TEXT,
            turn_index INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS moves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            player TEXT NOT NULL,
            r INTEGER,
            c INTEGER,
            direction TEXT,
            word TEXT,
            score INTEGER,
            move_number INTEGER
        );
        """)
        self.conn.commit()

    def insert_words(self, words: List[str]):
        self.cur.executemany("INSERT OR IGNORE INTO words(word) VALUES (?)", [(w,) for w in words])
        self.conn.commit()

    def word_exists(self, word: str) -> bool:
        self.cur.execute("SELECT 1 FROM words WHERE word = ?", (word.upper(),))
        return self.cur.fetchone() is not None

    def upsert_player(self, name: str):
        try:
            self.cur.execute("INSERT INTO players(name) VALUES (?)", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
