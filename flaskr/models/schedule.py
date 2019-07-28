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
        self.start_time     = helper.to_time(start_time)
        self.end_time       = helper.to_time(end_time)
        self.day_of_week    = helper.to_data(day_of_week)

class Schedule(db.Model):
    __tablename__   = 'schedule'
    id              = db.Column(db.Integer, primary_key=True)
    time_slots      = db.relationship('TimeSlot', secondary=associations.schedule_timeslot, 
                                        back_populates='schedules')

    def __init__(self, schedule_string):
        pass