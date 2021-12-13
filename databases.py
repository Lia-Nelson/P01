import sqlite3

class Permanent_databases:
    def __init__(self):
        connection = sqlite3.connect(file + ".txt")
        cursor = connection.cursor()
        cursor.execute(
        '''CREATE TABLE IF NOT EXISTS questions(
            question PRIMARY KEY,
            correct_answer TEXT NOT NULL,
            incorrect_answers TEXT NOT NULL
            )
        '''
        )
        cursor.execute(
        '''CREATE TABLE IF NOT EXISTS leaderboard(
            name PRIMARY KEY,
            score INTEGER NOT NULL
            )
        '''
        )
