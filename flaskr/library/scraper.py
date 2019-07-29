from flaskr.models.helper import DayOfWeek
from flaskr.models.schedule import TimeSlot, Schedule
from flaskr.models.instructor import Instructor
from flaskr.models.class_info import ClassInfo
from flaskr.models.class_schedule import ClassSchedule
from sqlalchemy import and_
from flaskr import db
from os import path, getenv
from ssl import SSLContext
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime

def scrape():
    sslcontext = SSLContext()
    curr_time = datetime.now().time()

    for page in range(ord('A'), ord('Z') + 1):
        for row in get_rows_from_page(page, sslcontext):
            if row.find('tr').text == "No classes to display":
                continue
            else:
                for idx, tr in enumerate(row.find_all('tr')):
                    cell = tr.find_all('td')
                    if idx == 0:
                        build_class_schedule(cell, curr_time)
                    else:
                        # for blocks but i'll ignore muna
                        pass
    
    print('database updated')

def get_rows_from_page(page, context):
    page_url = get_page_url(page)
    req = Request(page_url, headers = {'User-Agent': 'Mozilla/5.0'})
    html_data = urlopen(req, context=context).read()
    soup = BeautifulSoup(html_data, 'html.parser')

    table = soup.find(id = "tbl_schedule")
    return table.find_all('tbody')

def get_page_url(page):
    return path.join(getenv('SCHEDULE_URL'), chr(page))

def build_class_schedule(cell, curr_time):
    class_code = get_class_code(cell[0])
    class_info = get_class_info(cell)
    schedule = build_schedule(cell[3])
    instructors = get_instructors(cell[3])
    remarks = get_remarks(cell[3])
    available, total, demand = get_slots(cell)
    restrictions = get_restrictions(cell)

    class_schedule = ClassSchedule.query.filter(ClassSchedule.code == class_code).first()

    if class_schedule is None:
        class_schedule = ClassSchedule(class_code, class_info, schedule, instructors, available, total, demand,
                                        restrictions, remarks, curr_time)
        db.session.add(schedule)
    else:
        class_schedule.last_updated = curr_time
        
    db.session.commit()

def get_class_code(entry):
    return int(entry.text)

def get_class_info(cell):
    class_name = get_class_name(cell[1].text)
    credit = int(float(cell[2].text))

    class_info = ClassInfo.query.filter(ClassInfo.name == class_name).first()
    if class_info is None:
        class_info = ClassInfo(class_name, credit)
        db.session.add(class_info)
        db.session.commit()

    return class_info

def get_class_name(class_full_name):
    str_list = class_full_name.split()
    for idx, string in enumerate(str_list):
        if any(c.isdigit() for c in string):
            return ' '.join(str_list[:idx+1])

def build_schedule(schedule_entry):
    entries = schedule_entry.find('br').previous_sibling.strip().split(';')
    time_slots = []

    for entry in entries:
        if entry == 'TBA':
            pass
        else:
            tokens = entry.split()
            if tokens:
                day_list = get_day_list(tokens[0])
                start_time, end_time = get_time_window(tokens[1])
                time_slots += get_time_slot_list(day_list, start_time, end_time)

    return get_schedule(time_slots)

def get_day_list(dow):
    return [idx for idx, day in enumerate(DayOfWeek.dlist) if day != 'T' and day in dow or day in dow.replace('Th', '')]

def get_time_window(time_in_str):
    start_time, end_time = time_in_str.split('-')
    if 'M' not in start_time:
        start_time += end_time[-2:]
    return parse(start_time).time(), parse(end_time).time()
    
def get_time_slot_list(day_list, start_time, end_time):
    time_slots = []
    
    for day_of_week in day_list:
        time_slot = TimeSlot.query.filter(and_(
            TimeSlot.day_of_week == day_of_week,
            TimeSlot.start_time == start_time,
            TimeSlot.end_time == end_time
        )).first()

        if time_slot is None:
            time_slot = TimeSlot(start_time, end_time, day_of_week)
            db.session.add(time_slot)
            db.session.commit()
        
        time_slots.append(time_slot)

    return time_slots

def get_schedule(time_slots):
    schedules = Schedule.query.filter(and_(
        *[Schedule.time_slots.contains(time_slot) for time_slot in time_slots]
    )).all()

    schedule = None
    for sched in schedules:
        if len(sched.time_slots) == len(time_slots):
            schedule = sched
            break

    if schedule is None:
        schedule = Schedule(time_slots)
        db.session.add(schedule)
        db.session.commit()

    return schedule
    
def get_instructors(entry):
    instructors = []
    for instructor_name in entry.find('br').next_sibling.split(';'):
        instructor = Instructor.query.filter(Instructor.name == instructor_name.strip()).first()
        if instructor is None:
            instructor = Instructor(instructor_name.strip())
            db.session.add(instructor)
            db.session.commit()
        instructors.append(instructor)
    return instructors

def get_remarks(entry):
    return entry.find('em').text if entry.find('em') else None

def get_slots(cell):
    try:
        return int(cell[5].find('strong').text), int(cell[5].text.strip().split('/')[-1]), int(cell[6].text)
    except ValueError:
        return -1, -1, -1

def get_restrictions(cell):
    return cell[7].text if 7 < len(cell) else None