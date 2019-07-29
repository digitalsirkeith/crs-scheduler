from flaskr import db
from . import associations

class ClassSchedule(db.Model):
    __tablename__   = 'class_schedule'
    id              = db.Column(db.Integer, primary_key=True)
    code            = db.Column(db.Integer)
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
    remarks         = db.Column(db.Text)
    last_updated    = db.Column(db.Time)

    def __init__(self, code, class_info, schedule, instructors, 
                    available, total, demand, restrictions, remarks, last_updated):
        self.code               = code
        self.class_info_id      = class_info.id
        self.class_info         = class_info
        self.schedule_id        = schedule.id
        self.schedule           = schedule
        self.instructors        += instructors
        self.available_slots    = available
        self.total_slots        = total
        self.demand             = demand
        self.restrictions       = restrictions
        self.remarks            = remarks
        self.last_updated       = last_updated

    def __repr__(self):
        return '[{}] {} {} {} {}/{}/{} {} {}'.format(
            self.code,
            self.class_info,
            self.schedule,
            self.instructors,
            self.available_slots,
            self.total_slots,
            self.demand,
            self.restrictions,
            self.remarks
        )