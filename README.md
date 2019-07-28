# CRS Scheduler
I actually have no idea how to work this out.

Create a file named _.env_ and paste the following content:
```
FLASK_APP=flaskr
FLASK_ENV=development
DATABASE_URL=postgres://$(whoami)
```