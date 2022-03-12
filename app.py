from flask import (render_template,
    url_for, redirect, request)
from models import db, app, Project
import datetime

def clean_date(date):
    date_split = date.split('-')
    year = int(date_split[0])
    month = int(date_split[1])
    completion_date = datetime.date(year=year, month=month, day=1)

    return completion_date

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if request.form:
        new_project = Project(
            title=request.form['title'],
            date=clean_date(request.form['date']),
            description=request.form['desc'],
            skills=request.form['skills'],
            repo_link=request.form['github'])

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('index'))

    projects=Project.query.all()

    return render_template('projectform.html', projects=projects)

@app.route('/projects/<id>')
def project_detail(id):
    projects = Project.query.all()
    this_project = Project.query.get_or_404(id)

    return render_template('detail.html',
        projects=projects,
        this_project=this_project)

@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    this_project = Project.query.get_or_404(id)

    if request.form:
        this_project.title = request.form['title']
        this_project.date = clean_date(request.form['date'])
        this_project.description = request.form['desc']
        this_project.skills = request.form['skills']
        this_project.repo_link = request.form['github']

        db.session.commit()

        return redirect(url_for('index'))

    projects = Project.query.all()

    return render_template('projectform.html',
        projects=projects,
        this_project=this_project)

@app.route('/projects/<id>/delete')
def delete_project(id):
    this_project = Project.query.get_or_404(id)
    db.session.delete(this_project)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000, host='127.0.0.1')
