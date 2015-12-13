#!flask/bin/python
from app import app
from LogAnalyzer import *
#app.run(debug=True, port=80)
app.guild = Guild()
app.guild.load_from_json("./League_Of_Gunners.json-guild")
app.run(host="0.0.0.0")
