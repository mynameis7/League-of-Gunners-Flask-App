#!flask/bin/python
from app import app
from app.LogAnalyzer import *
app.guild = load_json_guild("./app/static/League_of_Gunners.json-guild")
app.run(debug=True, port=80)
#app.run(host="0.0.0.0")
