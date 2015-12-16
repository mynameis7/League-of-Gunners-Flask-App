from app import db

class Guildmate(db.Model):
    __tablename__ = "Guildmate"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(18), index=True, unique=True)
    rank_val = db.Column(db.Integer)
    in_guild = db.Column(db.Boolean)
    join_date = db.Column(db.DateTime)
    crown_deposits = db.relationship('CrownDeposits', backref='guildmate', lazy='select')
    energy_deposits = db.relationship('EnergyDeposits', backref='guildmate', lazy='select')
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.in_guild

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    

class Guild(db.Model):
    __tablename__ = "Guild"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class Logs(db.Model):
    __tablename__ = "Logs"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64))
    category = db.Column(db.String(32))
    name = db.Column(db.String(18))
    message = db.Column(db.String(512))
    new_name = db.Column(db.String(18))
    new_message = db.Column(db.String(512))


class Renames(db.Model):
    __tablename__ = "Renames"
    id = db.Column(db.Integer, primary_key=True)
    old = db.Column(db.String(18))
    new = db.Column(db.String(18))
    precedence = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('Guildmate.id'))


class CrownDeposits(db.Model):
    __tablename__ = "CrownDeposits"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('Guildmate.id'))
    date = db.Column(db.DateTime)
    value = db.Column(db.Integer)


class EnergyDeposits(db.Model):
    __tablename__ = "EnergyDeposits"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('Guildmate.id'))
    date = db.Column(db.DateTime)
    value = db.Column(db.Integer)
