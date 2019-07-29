# CRS Scheduler
I actually have no idea how to work this out.

Create a database named _scheduler_.
Create a file named _.env_ and paste the following content:
```
FLASK_APP=flaskr
FLASK_ENV=development
DATABASE_URL=postgres://localhost/scheduler
SECRET_KEY=dev
SCHEDULE_URL=https://crs.upd.edu.ph/schedule/120191/
```

Run the following commands:
```
flask db init
flask db migrate
flask db upgrade
```