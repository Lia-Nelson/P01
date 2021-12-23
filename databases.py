import sqlite3

class Databases:
    def __init__(self):
        connection = sqlite3.connect("perm.db")
        self.c = connection.cursor()
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS questions(
            question TEXT PRIMARY KEY,
            correct_answer TEXT NOT NULL,
            incorrect_answers TEXT NOT NULL
            );
        '''
        )
        self.c.execute(
        '''CREATE TABLE IF NOT EXISTS leaderboard(
            place INTEGER,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
            )
            ;
        '''
        )

    def add_question(self, question:str, correct_answer:str, incorrect_answers:str):
        Databases.debug_print(self, "Adding a question...")
        Databases.debug_print(self, question + "\n" + correct_answer + "\n" + incorrect_answers)
        # Retrieves question if it is in the database, otherwise returns none
        self.c.execute('''SELECT question FROM questions where question = ?;''', (question))
        q = self.c.fetchone()
        Databases.debug_print(self, "Question if it is already in the database: " + str(q))
        # If the question is not already in the database, inserts it into questiom
        # Else, updates the question so that the correct and incorrect answers are set to the
        # values most recently fed into add_question
        if (q == None):
            self.c.execute('''INSERT INTO questions VALUES(?, ?, ?);''', (question, correct_answer, incorrect_answers))
        else:
            self.c.execute('''
            UPDATE questions
                SET correct_answer = ?,
                    incorrect_answers = ?
                WHERE
                    question = ?;
            ''', (correct_answer, incorrect_answers, question))

    # Check to see if a certain score merits being on the leaderboard, only returns
    # true if the score is higher than the lowest score on the leaderboard or if
    # the leaderboard is not full
    def update_check(self, score:int) -> bool:
        self.c.execute('''SELECT min(score) FROM leaderboard;''')
        min = self.c.fetchone()
        min = min[0]
        need_update = False
        Databases.debug_print(self, "Minimum score in the leaderboard: " + str(min))
        # NEED TO FIX CHECK
        if (min == None):
            need_update = True
        else:
            self.c.execute('''SELECT max(place) FROM leaderboard;''')
            max = self.c.fetchone()
            max = max[0]
            Databases.debug_print(self, "Max place in the leaderboard: " + str(max))
            if (max < 5):
                need_update = True
            elif (score > min):
                need_update = True
        return need_update

    # Adds new entry into leaderboard, should only be run if score is higher than any
    # score in leaderboard
    def update_leaderboard(self, name:str, score:int):

        self.c.execute('''SELECT * FROM leaderboard;''')
        leaderboard = self.c.fetchall()
        Databases.debug_print(self, leaderboard)

        need_update = Databases.update_check(self, score)

        if (need_update):
            Databases.debug_print(self, "\nAdding a new score...")
            Databases.debug_print(self, "Name: " + name)
            # Deletes the entry in last place if it exists
            self.c.execute('''DELETE FROM leaderboard WHERE place = 5;''')
            self.c.execute('''SELECT score FROM leaderboard ORDER BY score;''')
            scores = self.c.fetchall()
            # Checks to make sure entry got added
            added = False
            # Inserts new leaderboard entry right below the first score that is higher than
            # or equal to it
            Databases.debug_print(self,"Scores: " + str(scores))
            for s in scores:
                Databases.debug_print(self, "Individual scores: " + str(s))
                # converts tuple to just the first value present (or score)
                Databases.debug_print(self, "First score : " + str(s[0]))
                if score <= s[0]:
                    self.c.execute('''SELECT max(place) FROM leaderboard WHERE score >= ?;''', str(s[0]))
                    place = self.c.fetchone()
                    place = place[0]
                    Databases.debug_print(self,"Maximum place with a score >= to the score we are adding " + str(place))
                    # must fix order goes through place
                    self.c.execute('''UPDATE leaderboard SET place = place + 1 WHERE place > ?;''', str(place))
                    self.c.execute('''INSERT INTO leaderboard VALUES(?, ?, ?);''', (place + 1, name, score))
                    added = True
                    break
            # If the entry did not get added (i.e. there are no higher scores), adds entry
            # into first place
            if not added:
                self.c.execute('''UPDATE leaderboard SET place = place + 1;''')
                self.c.execute('''INSERT INTO leaderboard(place, name, score)
                VALUES(?, ?, ?);''', (1, name, score))
        else: Databases.debug_print(self, "leadboard update not needed")

    def print_databases(self):
        Databases.print_database(self, "questions")
        Databases.print_database(self, "leaderboard")

    def print_database(self, database:str):
        command = '''SELECT * FROM ''' + database + ''';'''
        self.c.execute(command)
        database_data = self.c.fetchall()
        print(database + ": " + str(database_data))

    def return_leaderboard(self):
        self.c.execute('''SELECT * FROM leaderboard ORDER BY place;''')
        leaderboard_data = self.c.fetchall()
        return leaderboard_data

    def debug_print(self, message, debug:bool = False):
        if debug == True:
            print(message)
