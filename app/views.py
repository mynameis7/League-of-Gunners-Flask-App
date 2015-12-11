from flask import render_template
from app import app
import logmerger
import LogAnalyzer
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
        logs = app.guild.log
        print "Viewing Logs"
        #logs = logmerger.merge_all_logs(os.getcwd() + '/logs')
        return render_template("logsView.html",
                               title='View Logs',
                               logs=logs
                               )
