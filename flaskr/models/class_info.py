from flaskr import db
from . import associations

class ClassInfo(db.Model):
    __tablename__   = 'class_info'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.Text)
    units           = db.Column(db.Integer)
    class_schedules = db.relationship('ClassSchedule', back_populates='class_info')

    def __init__(self, name, units):
        self.name       = name
        self.units      = units

    def __repr__(self):
        return '{} ({})'.format(self.name, self.units)