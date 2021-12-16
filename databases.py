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

    # Adds new entry into leaderboard, should only be run if score is higher than any
    # score in leaderboard
    def update_leaderboard(self, name:str, score:int):
        # Deletes the entry in last place if it exists
        self.c.execute('''DELETE FROM leaderboard WHERE place = 5;''')
        self.c.execute('''SELECT score FROM leaderboard ORDER BY score;''')
        scores = self.c.fetchall()
        # Checks to make sure entry got added
        added = False
        # Inserts new leaderboard entry right below the first score that is higher it
        for s in scores:
            if score < s:
                self.c.execute('''SELECT min(place) FROM leaderboard WHERE score = s;''')
                place = self.c.fetchall()
                self.c.execute('''UPDATE leaderboard SET place = place - 1 WHERE place < ?;''', (place))
                self.c.execute('''INSERT INTO leaderboard(place, name, score)
                VALUES(?, ?, ?);''', (place-1, name, score))
                added = True
        # If the entry did not get added (i.e. there are no higher scores), adds entry
        # into first place
        if not added:
            self.c.execute('''INSERT INTO leaderboard(place, name, score)
            VALUES(?, ?, ?);''', (1, name, score))
