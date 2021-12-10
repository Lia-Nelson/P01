import sqlite3

class Databases:
    def __init__():
        create_leaderboard()
        create_questions()
        create_round()

    def create_database(file:str):
        connection = sqlite3.connect(file + ".txt")
        cursor = connection.cursor()
        # If does not work, construct string outside
        cursor.execute('''CREATE TABLE IF NOT EXISTS {{file}}
              (Title TEXT, Director TEXT, Year INT)''')
