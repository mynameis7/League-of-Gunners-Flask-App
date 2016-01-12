import sys, os
from app import db, models
path = "C:/Users/Andrew/Repositories/Github/League of Gunners App/src/"
if path not in sys.path:
    sys.path.append(path)
for p in sys.path:
    print p
from LogAnalyzer import *
from datetime import datetime
g = Guild()
g.load_from_json("League of Gunners.json-guild")

i = 0
for m in g.data.values():
    mem = models.Guildmate(id = i,
                           name = m.name,
                           rank_val = m.rank_val,
                           in_guild = m.in_guild,
                           join_date = m.join_date)
    db.session.add(mem)
    for cr in m.deposits:
        print mem.id
        d = models.CrownDeposits(player_id = i,
                                 date = cr[0],
                                 value = cr[1])
        db.session.add(d)
    for en in m.energy:
        e = models.EnergyDeposits(player_id = i,
                                 date = en[0],
                                 value = en[1])
        db.session.add(e)
    i += 1
for pair in g.renames:
    r = models.Renames(old = pair[0],
                       new = pair[1],
                       precedence = pair[2])
    db.session.add(r)

guild = models.Guild(name = g.name)
db.session.add(guild)

logs = g.log.data
logs.reverse()

for entry in logs:
    ev = models.Logs(date = entry.date,
                     category = entry.category,
                     name = entry.true_name,
                     message = entry.true_message,
                     new_name = entry.new_name,
                     new_message = entry.new_message)
    db.session.add(ev)

db.session.commit()
