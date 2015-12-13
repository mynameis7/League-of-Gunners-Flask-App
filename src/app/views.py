from flask import render_template
from app import app
import os
@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
				title='Home',
                                guild=app.guild,
				)

@app.route('/viewlogs')
def logsView():
        print "Viewing Logs"
        #logs = logmerger.merge_all_logs(os.getcwd() + '/logs')
        return render_template("logsView.html",
                               title='View Logs',
                               guild=app.guild
                               )
