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
            place INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
            );
        '''
        )

    def add_question(self, question:str, correct_answer:str, incorrect_answers:str):
        print(question + "\n" + correct_answer + "\n" + incorrect_answers)
        self.c.execute(
        '''INSERT INTO questions(question, correct_answer, incorrect_answers)
        VALUES(?, ?, ?);''', (question, correct_answer, incorrect_answers))

    # Adds new entry into leaderboard, should only be run if score is higher than any
    # score in leaderboard
    def update_leaderboard(self, name:str, score:int):
        print("Name: " + name)
        # Deletes the entry in last place if it exists
        self.c.execute('''DELETE FROM leaderboard WHERE place = 5;''')
        self.c.execute('''SELECT score FROM leaderboard ORDER BY score;''')
        scores = self.c.fetchall()
        # Checks to make sure entry got added
        added = False
        # Inserts new leaderboard entry right below the first score that is higher than
        # or equal to it
        #print(scores)
        for s in scores:
            # converts tuple to just the first value present (or score)
            if score <= s[0]:
                self.c.execute('''SELECT max(place) FROM leaderboard WHERE score = s;''')
                place = self.c.fetchone()
                print("Maximum place with a score >= to the score we are adding" + place[0])
                # must fix order goes through place
                self.c.execute('''UPDATE leaderboard SET place = place + 1 WHERE place > ?;''', (place))
                self.c.execute('''INSERT INTO leaderboard(place, name, score)
                VALUES(?, ?, ?);''', (place + 1, name, score))
                added = True
        # If the entry did not get added (i.e. there are no higher scores), adds entry
        # into first place
        if not added:
            self.c.execute('''UPDATE leaderboard SET place = place + 1;''')
            self.c.execute('''INSERT INTO leaderboard(place, name, score)
            VALUES(?, ?, ?);''', (1, name, score))

    def print_databases(self):
        self.c.execute('''SELECT * FROM questions;''')
        questions = self.c.fetchall()
        print(questions)
        self.c.execute('''SELECT * FROM leaderboard;''')
        leaderboard = self.c.fetchall()
        print(leaderboard)
