from flaskr import db
from . import  associations

class Instructor(db.Model):
    __tablename__   = 'instructor'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.Text)
    class_schedules = db.relationship('ClassSchedule', secondary=associations.instructor_class_schedule, 
                                        back_populates='instructors')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name