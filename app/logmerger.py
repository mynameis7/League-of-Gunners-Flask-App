from datetime import datetime
import datetime as dt
import csv
import itertools
import multiprocessing as mp
import os


TAGS = ("Membership", "Treasury", "Storage", "Energy", "Upkeep", "Guild Hall")


class Event(object):
    def __init__(self, (d, c, n, m)):
        #4 sections that the guild log has.
        self.date = d
        self.category = c
        self.name = n
        self.message = m

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return str(self) == str(other)
        else:
            return False

    def __str__(self):
        return self.get_csv_string()

    def get_csv_string(self):
        return '"%s","%s","%s","%s"' % (self.date, self.category, self.name, self.message)

def get_datetime_from_stamp(timestamp):
    formatstr = '%m/%d/%y %I:%M:%S %p'
    date = datetime.strptime(timestamp, formatstr)
    return date

class EventList(object):
    #list of all the events retrieved from a guild log
    def __init__(self):
        self.data = []
        self.headers = ('Timestamp', 'Category', 'Name', 'Message')

    def add(self, evt):
        if not self.event_in_list(evt):
            self.data.append(evt)
            
    def get_filtered(self, string):
        return filter(lambda x: x.category == string, self.data)

    def event_in_list(self, ev):
        for event in self.data:
            if ev == event:
                return True
        return False

    def export_list(self, filepath):
        with open(filepath, 'w') as f:
            f.write('"%s","%s","%s","%s"' % self.headers + '\n')
            for event in self.data:
                f.write(event.get_csv_string() + "\n")

    def get(self):
        newdict = {'data': [i.__dict__ for i in self.data],
                   'headers': self.headers}
        return newdict

    def order(self):
        
        self.data = sorted(self.data, key=lambda ev: get_datetime_from_stamp(ev.date), reverse=True)


def extract_data(data):
    #You send it the filepath to the Spiral Knights Log csv
    with open(data) as f:
        c = csv.reader(f)
        d = [i for i in c]

    datalist2 = EventList()
    for i in d[1:]:
        datalist2.add(Event(i))
    
    return datalist2

def get(log):
    with open(log) as f:
        c = csv.reader(f)
        d = [i for i in c]
        return d[1:]

def add_log_to_guild(mainlog, filepaths):
##    size = mp.cpu_count()
##    p1 = mp.Pool(processes=size)
##    data = p1.map(get, filepaths)
##    data = list(itertools.chain.from_iterable(data))
##    print "events retrieved"
##    p2 = mp.Pool(processes=size)
##    events = p2.map(Event, data)
##    print "events parsed"
    events = []
    for name in filepaths:
        data = get(name)
        for line in data:
            events.append(Event(line))
    for evt in events:
        mainlog.add(evt)
    print "events added"
    #for i in filepaths:
    #    l = extract_data(i)
    #    for evt in l.data:
    #        mainlog.add(evt)
    mainlog.order()

def save(g):
    g.save_to_file(g.filepath)


def merge_all_logs(logpath):
    log = EventList()
    inputs = []
    for path, dirnames, filenames in os.walk(logpath):
        for i in filenames:
            inputs.append( os.path.join(path, i))
    add_log_to_guild(log, inputs)
    return log


if __name__ == "__main__":
    import os
    log = EventList()
    logpath1 = os.getcwd()+"\\logs"
    inputs = []
    for path, dirnames, filenames in os.walk(logpath1):
        for i in filenames:
            inputs.append( os.path.join(path, i))
    add_log_to_guild(log, inputs)
    log.export_list("log.csv")
##    import qtLog_Analyzer_GUI_V2 as gui
##    import sys
##    app = gui.QApplication(sys.argv)
##    ui = gui.Compiled_UI()
##    ui.guild = guild
##    ui.update()
##    sys.exit(app.exec_())
