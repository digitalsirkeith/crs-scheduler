from flaskr import db
from datetime import datetime
from . import helper, associations

class TimeSlot(db.Model):
    __tablename__   = 'time_slot'
    id              = db.Column(db.Integer, primary_key=True)
    start_time      = db.Column(db.Time)
    end_time        = db.Column(db.Time)
    day_of_week     = db.Column(db.Integer)
    schedules       = db.relationship('Schedule', secondary=associations.schedule_timeslot, 
                                        back_populates='time_slots')

    def __init__(self, start_time, end_time, day_of_week):
        self.start_time     = start_time
        self.end_time       = end_time
        self.day_of_week    = day_of_week

    def __repr__(self):
        return '{} {}-{}'.format(helper.to_str(self.day_of_week), self.start_time, self.end_time)

class Schedule(db.Model):
    __tablename__   = 'schedule'
    id              = db.Column(db.Integer, primary_key=True)
    time_slots      = db.relationship('TimeSlot', secondary=associations.schedule_timeslot, 
                                        back_populates='schedules')

    def __init__(self, time_slots):
        self.time_slots += time_slots

    def __repr__(self):
        return '|'.join([str(time_slot) for time_slot in self.time_slots])