from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, models, lm
from datetime import datetime as dt
import requests
from postmarkup import render_bbcode

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
        guildmaster = models.Guildmate.query.filter(models.Guildmate.rank_val == 4).filter(models.Guildmate.in_guild == True)
        officer = models.Guildmate.query.filter(models.Guildmate.rank_val == 3).filter(models.Guildmate.in_guild == True)
        veteran = models.Guildmate.query.filter(models.Guildmate.rank_val == 2).filter(models.Guildmate.in_guild == True)
        member = models.Guildmate.query.filter(models.Guildmate.rank_val == 1).filter(models.Guildmate.in_guild == True)
        recruit = models.Guildmate.query.filter(models.Guildmate.rank_val == 0).filter(models.Guildmate.in_guild == True)

        mems = {"Guild Master": guildmaster,
                "Officer": officer,
                "Veteran": veteran,
                "Member": member,
                "Recruit": recruit}
        return mems

ranks = {0: "Recruit",
         1: "Member",
         2: "Veteran",
         3: "Officer",
         4: "Guild Master"}

@app.template_global()
def get_user_rank(user):
    return ranks[user.rank_val]

template="default/"

@app.route('/')
@app.route('/index')
def index():
    base = get_base_vars()
    mems = get_members_by_rank()
    #news = requests.get("http://logunners.shivtr.com/news_entries.json")
    news = requests.get("https://raw.githubusercontent.com/mynameis7/League-of-Gunners-Flask-App/master/src/app/static/news_entries.json")
    print type(news.json())
    entries = news.json()["news_entries"]
    for i in xrange(len(entries)):
        entry = entries[i]
        entry["entry"] = render_bbcode(entry["entry"])
    print len(entries)
    return render_template(template + "index.html",
                title='Home',
                                name=base["name"],
                                short_name=base["short"],
                                members=mems,
                                template=template,
                                news=entries
                )

@app.route('/viewlogs')
@login_required
def logsView():
        print "Viewing Logs"
        #logs = logmerger.merge_all_logs(os.getcwd() + '/logs')
        logs = models.Logs.query.all()
        logs.reverse()
        base = get_base_vars()
        return render_template(template + "logsView.html",
                               title='View Logs',
                               name=base["name"],
                               short_name=base["short"],
                               logs=logs,
                               log_len=len(logs),
                               template=template
                               )

@app.route('/about')
def about():
        base = get_base_vars()
        return render_template(template + "about.html",
                               title="Charter",
                               name=base["name"],
                               short_name=base["short"],
                               template=template)


@lm.user_loader
def load_user(id):
    return models.Guildmate.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/unauthorized')
def unauthorized():
    return redirect(url_for("index"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "GET":
        base = get_base_vars()
        return render_template(template + 'login.html',
                                title="login",
                                name=base["name"],
                                short_name=base["short"],
                                template = template)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember = False
        if 'remember' in request.form:
            remember = True
        user = models.Guildmate.query.filter(models.Guildmate.name == username).first()
        if user is not None:
            login_user(user, remember=remember)
            flash('logged in successfully')
            next = request.args.get('next')
            #if not next_is_valid(next):
            #    return flask.abort(400)
            return redirect( next or url_for('index'))
        else:
            return redirect(url_for('unauthorized'))
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/member/<name>")
@login_required
def profile(name):
    user = models.Guildmate.query.filter(models.Guildmate.name == name).first()
    base = get_base_vars()
    joindate = user.join_date.strftime("%m-%d-%Y %H:%M")
    days_in = (dt.now() - user.join_date).days
    total_d = sum( [ dep.value for dep in user.crown_deposits ])
    logs = models.Logs.query.all()
    userlogs = [log for log in logs if log.current_name == name]
    return render_template(template + "member.html",
                            itle=name,
                            name=base["name"],
                            short_name=base["short"],
                            user=user,
                            user_joindate=joindate,
                            days=days_in,
                            total_crowns=total_d,
                            logs=userlogs,
                            template=template)