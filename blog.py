from flask import (Flask, render_template, request, session, flash, 
					redirect, url_for, g)
from functools import wraps

import sqlite3

DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'

SECRET_KEY = '\xf4\xf2\xea\x7f\xf2\x93\xc6\x1a\x9b8P\xeb[\x03\x83\xbb\xc9\xe1Kg`\x03\xf3G'

app = Flask(__name__)

app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to be logged in first')
			return redirect(url_for('login'))
	return wrap 

@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or \
			request.form['password'] != app.config['PASSWORD']:
				error = 'Invalid Credentials.'
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	return render_template('login.html', error=error)

@app.route('/main')
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
	g.db.close()
	return render_template('main.html', posts=posts)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields are required")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('insert into posts (title, post) values (?, ?)', 
			[request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash("New entry was posted")
		return redirect(url_for('main'))




if __name__ == '__main__':
	app.run(debug=True)

