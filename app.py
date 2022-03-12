from flask import (render_template,
    url_for, redirect, request)
from models import db, app, Project


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000, host='127.0.0.1')
