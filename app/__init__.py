from flask import Flask

app = Flask(__name__)
from app import views
import LogAnalyzer
import LogAnalyzer as SK
from LogAnalyzer import *
app.guild = SK.Guild()
app.guild.load_from_file("./League_Of_Gunners.guild")
