# Tests the databases
import sys
from os import remove, path
# adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from databases import Permanent_databases
import random

def purge():
	global d
	global db_file
	db_file = "perm.db"
	if path.exists(db_file):
		remove(db_file) #makes sure none of previous test is there
		d = Permanent_databases()
	else:
		d = Permanent_databases()

purge()

def show_result(success:bool):
	if success:
  		print("Success")
	else:
  		print("Failed")

def test_question_creation(num:int = 100):
	success = False
	print("Testing question creation...")
	try:
		for i in range(num):
			d.add_question(str(i), str(i), str(i))
			success = True
	except Exception as e:
		print(e)
	return show_result(success)

def test_leaderboard_update(num:int=100):
	success = False
	print("Testing leaderboard update...")
	try:
		for i in range(num):
			d.update_leaderboard(str(i), 10 - (i % 10))
			success = True
	except Exception as e:
		print(e)
	return show_result(success)

test_question_creation(5)

test_leaderboard_update(10)

d.print_databases()
