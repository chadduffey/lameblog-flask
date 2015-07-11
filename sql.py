import sqlite3

with sqlite3.connect("blog.db") as connection:

	c = connection.cursor()

	c.execute("""CREATE TABLE posts (title TEXT, post TEXT)""")

	c.execute('INSERT INTO posts VALUES("Good", "Im good")')
	c.execute('INSERT INTO posts VALUES("Well", "Im well")')
	c.execute('INSERT INTO posts VALUES("Excellent", "Im excellent")')
	c.execute('INSERT INTO posts VALUES("Okay", "Im okay")')

