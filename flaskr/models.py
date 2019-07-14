from sqlalchemy import Integer, Text, Column, Time
from flaskr.database import Base

class ClassShedule(Base):
    __tablename__   = 'class_schedules'
    id              = Column(Integer, primary_key=True)
    class_code      = Column(Integer, nullable=False)
    class_name      = Column(Text)
    instructor      = Column(Text)
    units           = Column(Integer)
    restrictions    = Column(Text)
    available_slots = Column(Integer)
    total_slots     = Column(Integer)
    demand          = Column(Integer)
    start_time      = Column(Time)
    end_time        = Column(Time)


    def __init__(self, class_code=-1, 
                        class_name='?', 
                        instructor='CONCEALED', 
                        units=0,
                        restrictions='',
                        available_slots=0,
                        total_slots=0,
                        demand=0,
                        start_time=None,
                        end_time=None):

        self.class_code         = class_code
        self.class_name         = class_name
        self.instructor         = instructor
        self.units              = units
        self.restrictions       = restrictions
        self.available_slots    = available_slots
        self.total_slots        = total_slots
        self.demand             = demand
        self.start_time         = start_time
        self.end_time           = end_time

    def __repr__(self):
        return '[{0}][{5}/{6}/{7}][{8}-{9}] {1} {2} {3}.0 ({4})'.format(
            self.class_code,
            self.class_name,
            self.instructor,
            self.units,
            self.restrictions,
            self.available_slots,
            self.total_slots,
            self.demand,
            self.start_time,
            self.end_time
        )