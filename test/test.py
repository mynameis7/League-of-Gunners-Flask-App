import sys, os

path= os.path.abspath(os.path.join("../", "src"))
if path not in sys.path:
    sys.path.append(path)
from app import db, models, views

mems = db.session.query(models.Guildmate).all()
mems = views.get_members_by_rank()
