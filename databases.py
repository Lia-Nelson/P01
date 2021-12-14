import sqlite3

class Permanent_databases:
    def __init__(self):
        connection = sqlite3.connect(file + ".txt")
        self.c = connection.cursor()
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS questions(
            question PRIMARY KEY,
            correct_answer TEXT NOT NULL,
            incorrect_answers TEXT NOT NULL
            )
        '''
        )
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS leaderboard(
            name PRIMARY KEY,
            score INTEGER NOT NULL
            )
        '''
        )

    def add_question(self, question:str, correct_answer:str, incorrect_answers:str):
        self.c.execute(
        '''INSERT INTO questions(
            question,
            correct_answer,
            incorrect_answers
            )
        '''
        )
