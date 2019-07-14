export FLASK_APP=flaskr
export FLASK_ENV=development
export DATABASE_URL=postgres://localhost/$(whoami)
flask init-db