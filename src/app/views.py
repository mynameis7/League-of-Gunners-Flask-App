from flask import render_template
from app import app, models


def get_base_vars():
        name = models.Guild.query.all()[0].name
        temp = name.split(" ")
        short = ""
        for word in temp:
                short += word[0]
        d = {}
        d["short"] = short
        d["name"] = name
        return d

def get_members_by_rank():
        guildmaster = models.Guildmate.query.filter(models.Guildmate.rank_val == 4 and models.Guildmate.in_guild == True)
        officer = models.Guildmate.query.filter(models.Guildmate.rank_val == 3 and models.Guildmate.in_guild == True)
        veteran = models.Guildmate.query.filter(models.Guildmate.rank_val == 2 and models.Guildmate.in_guild == True)
        member = models.Guildmate.query.filter(models.Guildmate.rank_val == 1 and models.Guildmate.in_guild == True)
        recruit = models.Guildmate.query.filter(models.Guildmate.rank_val == 0 and models.Guildmate.in_guild == True)

        mems = {"Guild Master": guildmaster,
                "Officer": officer,
                "Veteran": veteran,
                "Member": member,
                "Recruit": recruit}
        return mems





@app.route('/')
@app.route('/index')
def index():
    base = get_base_vars()
    mems = get_members_by_rank()
    return render_template("index.html",
                title='Home',
                                name=base["name"],
                                short_name=base["short"],
                                members=mems
                )

@app.route('/viewlogs')
def logsView():
        print "Viewing Logs"
        #logs = logmerger.merge_all_logs(os.getcwd() + '/logs')
        logs = models.Logs.query.all()
        logs.reverse()
        base = get_base_vars()
        return render_template("logsView.html",
                               title='View Logs',
                               name=base["name"],
                               short_name=base["short"],
                               logs=logs,
                               )

@app.route('/about')
def about():
        base = get_base_vars()
        return render_template("about.html",
                               title="Charter",
                               name=base["name"],
                               short_name=base["short"])
