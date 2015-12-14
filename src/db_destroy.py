import os, shutil

try:
    os.remove("./app.db")
except: pass
try:
    shutil.rmtree("./db_repository")
except Exception as e:
    print e
    
