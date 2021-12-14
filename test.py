# Tests the databases
import sys
from os import remove, path
# adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#imports from ../app/story_manager.py
from app.databases import Permanent_databases
import random

print(path.dirname(path.abspath(__file__)))
db_file = path.dirname(path.abspath(__file__)) + "/test.db"
sm = None

def purge():
	global sm
	global db_file
	if path.exists(db_file):
		del sm
		remove(db_file) #makes sure none of previous test is there
		sm = Story_manager(db_file)
	else:
		sm = Story_manager(db_file)

purge()

def test_creation(num:int = 100):
	global sm
	success = False
	print("___ test create_story ___")
	print("~~ NO DUPES ~~")
	try:
		for i in range(num):
			sm.create_story("test", str(i), str(i))
	except Exception as e:
		print(e)
		return success

    if success:
  	print("Success")
  else:
  	print("Failed")
