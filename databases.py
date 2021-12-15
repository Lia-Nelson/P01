import sqlite3

class Permanent_databases:
    def __init__(self):
        connection = sqlite3.connect("perm.db")
        self.c = connection.cursor()
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS questions(
            question PRIMARY KEY,
            correct_answer TEXT NOT NULL,
            incorrect_answers TEXT NOT NULL
            );
        '''
        )
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS leaderboard(
            place PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
            );
        '''
        )

    # def debug_print(input, DEBUG:bool = True):
    #     if DEBUG:
    #         print(input)

    def add_question(self, question:str, correct_answer:str, incorrect_answers:str):
        #debug_print(question + "\n" + correct_answer + "\n" + incorrect_answers)
        self.c.execute(
        '''INSERT INTO questions(question, correct_answer, incorrect_answers)
        VALUES(?, ?, ?);''', (question, correct_answer, incorrect_answers))

    def update_leaderboard(self, name:str, score:int):
        self.c.execute('''DELETE FROM leaderboard WHERE place = 5;''')
        self.c.execute('''SELECT score FROM leaderboard ORDER BY (score);''')
        scores = self.c.fetchall()
        print(scores)
