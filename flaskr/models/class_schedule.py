from flaskr import db
from . import associations

class ClassInfo(db.Model):
    __tablename__   = 'class_info'
    id              = db.Column(db.Integer, primary_key=True)
    code            = db.Column(db.Integer)
    name            = db.Column(db.Text)
    units           = db.Column(db.Integer)
    class_schedules = db.relationship('ClassSchedule', back_populates='class_info')

    def __init__(self, code, class_name, units):
        self.code       = code
        self.class_name = class_name
        self.units      = units

class ClassSchedule(db.Model):
    __tablename__   = 'class_schedule'
    id              = db.Column(db.Integer, primary_key=True)
    class_info_id   = db.Column(db.Integer, db.ForeignKey('class_info.id'))
    class_info      = db.relationship('ClassInfo', back_populates='class_schedules')
    schedule_id     = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    schedule        = db.relationship('Schedule')
    instructors     = db.relationship('Instructor', secondary=associations.instructor_class_schedule, 
                                        back_populates='class_schedules')
    available_slots = db.Column(db.Integer)
    total_slots     = db.Column(db.Integer)
    demand          = db.Column(db.Integer)
    restrictions    = db.Column(db.Text)

    def __init__(self):
        pass

class Block(db.Model):
    __tablename__   = 'block'
    id              = db.Column(db.Integer, primary_key=True)
    class_schedules = db.relationship('ClassSchedule', secondary=associations.block_class_schedule)

    def __init__(self):
        pass


    # def __init__(self, class_code=-1, 
    #                     class_name='?', 
    #                     instructor='CONCEALED', 
    #                     units=0,
    #                     restrictions='',
    #                     available_slots=0,
    #                     total_slots=0,
    #                     demand=0,
    #                     start_time=None,
    #                     end_time=None):

    #     self.class_code         = class_code
    #     self.class_name         = class_name
    #     self.instructor         = instructor
    #     self.units              = units
    #     self.restrictions       = restrictions
    #     self.available_slots    = available_slots
    #     self.total_slots        = total_slots
    #     self.demand             = demand
    #     self.start_time         = start_time
    #     self.end_time           = end_time