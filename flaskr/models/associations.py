from flaskr import db

schedule_timeslot = db.Table('schedule_timeslot_association',
    db.Column('time_slot_id', db.Integer, db.ForeignKey('time_slot.id')),
    db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id'))
)

instructor_class_schedule = db.Table('instructor_class_schedule_association',
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id')),
    db.Column('class_schedule_id', db.Integer, db.ForeignKey('class_schedule.id'))
)

block_class_schedule = db.Table('block_class_schedule_association',
    db.Column('block_id', db.Integer, db.ForeignKey('block.id')),
    db.Column('class_schedule_id', db.Integer, db.ForeignKey('class_schedule.id'))
)