from app import db, models, app
import csv
from datetime import datetime
import re


def extract_data(data):
    # You send it the filepath to the Spiral Knights Log csv
    with open(data) as f:
        c = csv.DictReader(f)
        d = [i for i in c]

    return d


def process_log(entries):
    for entry in entries:
        category = entry["Category"]
        if category == "Membership":
            process_membership(entry)
        elif category == "Treasury":
            process_treasury(entry)
        elif category == "Energy":
            process_energy(entry)
        elif category == "Storage":
            pass


def map_rank(_in):
    str_to_int = {
        "Recruit": 0,
        "Member": 1,
        "Veteran": 2,
        "Officer": 3,
        "Guild Master": 4
        }
    int_to_str = [
        "Recruit",
        "Member",
        "Veteran",
        "Officer",
        "Guild Master"
        ]
    if type(_in) == int:
        return int_to_str[_in]
    elif type(_in) == str:
        return str_to_int[_in]
    else:
        raise Exception("Type mismatch for mapping rank")


def process_membership(event):
    def rank_analyzer(mssg):
        rank_re = re.compile("(Promoted|Demoted) (.*) to (Recruit|Member|Veteran|Officer|Guild Master)")
        return rank_re.match(mssg).groups()

    def removed_analyzer(mssg):
        removed_re = re.compile("Removed (.*) from the guild.")
        return removed_re.match(mssg).groups()[0].strip()

    def accepted(event):
        name = event["Name"]
        q = db.session.query(models.Guildmate).filter(models.Guildmate.name == name)
        mems = q.all()
        member = None
        joindate = convert(event["Timestamp"])
        if len(mems) == 1:
            member = mems[0]
            member.rank_val = 0
            member.in_guild = True
            member.join_date = joindate
            #db.session.commit()
        elif len(mems) == 0:
            member = models.Guildmate(name = name,
                                      rank_val = 0,
                                      in_guild = True,
                                      join_date = joindate)
            #db.session.add(member)
            #db.session.commit()
        else:
            raise Exception("Database irregularity, duplicate member name")

    def rank(event):
        shift, name, _rank = rank_analyzer(event["Message"])
        q = db.session.query(models.Guildmate).filter(models.Guildmate.name == name)
        mems = q.all()
        new_rank = map_rank(_rank)
        if len(mems) == 1:
            member = mems[0]
            member.rank_val = new_rank
            #db.session.commit()
        elif len(mems) == 0:
            joindate = convert(event["Timestamp"])
            member = models.Guildmate(name = name,
                                      rank_val = new_rank,
                                      in_guild = True,
                                      join_date = joindate)
            #db.session.add(member)
            #db.session.commit()
        else:
            raise Exception("Database irregularity, duplicate member name")    
        
    def removed(event):
        name = removed_analyzer(event["Message"])
        q = db.session.query(models.Guildmate).filter(models.Guildmate.name == name)
        mems = q.all()        
        if len(mems) == 1:
            member = mems[0]
            member.in_guild = False
            #db.session.commit()
        elif len(mems) == 0:
            joindate = convert(event["Timestamp"])
            member = models.Guildmate(name = name,
                                      rank_val = 0,
                                      in_guild = False,
                                      join_date = joindate)
            #db.session.add(member)
            #db.session.commit()
        else:
            raise Exception("Database irregularity, duplicate member name")  

    def left(event):
        name = event["Name"]
        q = db.session.query(models.Guildmate).filter(models.Guildmate.name == name)
        mems = q.all()        
        if len(mems) == 1:
            member = mems[0]
            member.in_guild = False
            #db.session.commit()
        elif len(mems) == 0:
            joindate = convert(event["Timestamp"])
            member = models.Guildmate(name = name,
                                      rank_val = 0,
                                      in_guild = False,
                                      join_date = joindate)
            #db.session.add(member)
            #db.session.commit()
        else:
            raise Exception("Database irregularity, duplicate member name")  
        
    member_re = re.compile("(Accepted|Promoted|Demoted|Removed|Left)")
    topic = member_re.match(event["Message"]).group()
    if topic == "Accepted":
        accepted(event)
    if topic == "Promoted" or topic == "Demoted":
        rank(event)
    if topic == "Removed":
        removed(event)
    if topic == "Left":
        left(event)
def process_treasury(event):
    pass
def process_energy(event):
    pass
def process_storage(event):
    pass

_cmp = lambda x, y: 1 if convert(x["Timestamp"]) < convert(y["Timestamp"]) else 0 if convert(x["Timestamp"]) == convert(y["Timestamp"]) else -1
def convert(timestamp):
    formatstr = '%m/%d/%y %I:%M:%S %p'
    date = datetime.strptime(timestamp, formatstr)
    return date

def get_new_entries(filepath):
    new_logs = []
    logs = extract_data(filepath)
    for log in logs:
        q = db.session.query(models.Logs).filter(models.Logs.date==log["Timestamp"],
                                                 models.Logs.category==log["Category"],
                                                 models.Logs.name==log["Name"],
                                                 models.Logs.message==log["Message"])
        if not db.session.query(q.exists()).scalar():
            new_logs.append(log)
    return new_logs

def run_dev_server():
    app.run(debug=True)

entries = get_new_entries("League_Of_Gunners_2015-12-23_21-09-13.csv")
entries.sort(cmp=_cmp, reverse=True)
process_log(entries)
