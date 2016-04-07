from flask import Flask, render_template, flash, redirect, url_for
from forms import SearchForm
import sqlite3
import time_series as ts

app = Flask(__name__)
app.config.from_object('config')
app.debug = True

@app.route('/')
def route2home():
	return redirect('/hrc-ee')

@app.route('/hrc-ee/',methods=['GET','POST'])
def route2hello():
	return redirect(url_for('.hello', stype='bs'))

@app.route('/hrc-ee/<stype>', methods=['GET','POST'])
#@app.route('/')
def hello(stype):
	form = SearchForm()
#	print "past form"
	#return "heyo"
	if form.validate_on_submit():
		flash('Searching Hillary\'s emails for "%s"' % 
              	(form.search.data ))
		#stype as placeholder in case we want to add different seach schemes
		#'bs' = body/subject
		#'ps' = people search 
		#'es' = email search (to/from address)
        	return redirect(url_for('.search',stype = stype, search = form.search.data))
	#form = 'skdfjl'
	return render_template('index.html', stype = stype, form = form, search_types = app.config['SEARCH_TYPES'])

#Search page.  Queries DB, returns results

@app.route('/hrc-ee/search/<stype>/<search>', methods = ['GET','POST'])
def search(stype, search):
	body_rows = search_bs(search)	
	form = SearchForm()
#	print "past form"
	#return "heyo"
	if form.validate_on_submit():# and request.method == 'POST':
		flash('Searching Hillary\'s emails for "%s"' % 
              	(form.search.data ))
		#stype as placeholder in case we want to add different seach schemes
		#'bs' = body/subject
		#'ps' = people search 
		#'es' = email search (to/from address)
        	return redirect(url_for('.search', stype = stype, search = form.search.data))
	
	return render_template('search.html', results = body_rows, stype = stype, form = form)
	
def search_bs(search):
	db_name = '01_database/hrc.sqlite'
	db = sqlite3.connect(db_name)
	#Force name-base access to rows.  Excellent for templates
	db.row_factory = sqlite3.Row

	cursor = db.cursor()

	#Sanitize input.  Perhaps the searches can be broken up by words later
	#search = sanitize(search)
	search = "%" + search + "%"
	sql_cmd = 'SELECT * FROM emails \
	  	   WHERE (ExtractedBodyText LIKE ?\
			  OR ExtractedSubject LIKE ?)'
	cursor.execute(sql_cmd, (search, search))
	rows = cursor.fetchall()
	return rows

#Raw email display
@app.route('/hrc-ee/raw_email/<stype>/<docnumber>', methods = ['GET', 'POST'])
def raw_email(stype,docnumber):
	#Get the raw email from the database
	db_name = '01_database/hrc.sqlite'
	db = sqlite3.connect(db_name)
	cursor = db.cursor()

	#search = docnumber
	sql_cmd = 'SELECT RawText FROM emails\
		   WHERE DocNumber IS ?'
	cursor.execute(sql_cmd, (docnumber,))
	tmp = cursor.fetchone()
	raw_email = tmp[0]
	#Remove special characters and split into lines:
	evec = raw_email.split('\n')
	for line in evec:
		line.strip()
	#Take care of search form
	form = SearchForm()
	if form.validate_on_submit():# and request.method == 'POST':
		flash('Searching Hillary\'s emails for "%s"' % 
              	(form.search.data ))
		#stype as placeholder in case we want to add different seach schemes
		#'bs' = body/subject
		#'ps' = people search 
		#'es' = email search (to/from address)
        	return redirect(url_for('.search', stype = stype, search = form.search.data))

	return render_template('raw_email.html',
				raw_email = evec,
				docnumber = docnumber,
				form = form)
@app.route('/hrc-ee/email/<stype>/<docnumber>', methods = ['GET','POST'])
def email(stype, docnumber):
	#Get the raw email from the database
	db_name = '01_database/hrc.sqlite'
	db = sqlite3.connect(db_name)
	cursor = db.cursor()

	#search = docnumber
	sql_cmd = 'SELECT ExtractedBodyText FROM emails\
		   WHERE DocNumber IS ?'
	cursor.execute(sql_cmd, (docnumber,))
	raw_email = cursor.fetchone()

	#Take care of search form
	form = SearchForm()
	if form.validate_on_submit():# and request.method == 'POST':
		flash('Searching Hillary\'s emails for "%s"' % 
              	(form.search.data ))
		#stype as placeholder in case we want to add different seach schemes
		#'bs' = body/subject
		#'ps' = people search 
		#'es' = email search (to/from address)
        	return redirect(url_for('.search', stype = stype, search = form.search.data))

	return render_template('raw_email.html',
				raw_email = raw_email,
				docnumber = docnumber,
				form = form)

#Visualization / Data mining pieces / scripts / etc
@app.route('/hrc-ee/vis/')
def vis_home():
	figure = ts.test_function()
	return render_template('vis_home.html', figure = figure)


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=9000)
