import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
            os.getenv('MYSQL_DATABASE'), 
            user=os.getenv('MYSQL_USER'), 
            password=os.getenv('MYSQL_PASSWORD'), 
            host=os.getenv('MYSQL_HOST'), 
            port=3306
)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
            os.getenv('MYSQL_DATABASE'), 
            user=os.getenv('MYSQL_USER'), 
            password=os.getenv('MYSQL_PASSWORD'), 
            host=os.getenv('MYSQL_HOST'), 
            port=3306
        )
    
print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb

mydb.connect()
print(mydb)
mydb.create_tables([TimelinePost])

hobbiesArray = [{
    "name": "Coding",
    "description": "I like coding and learning new things. I am currently learning how to use Flask and about deploying microservices.",
    "image": "static/img/coding.jpeg"
},{
    "name": "Reading",
    "description": "I love reading books. I am currently reading 'The 7 Habits of Highly Effective People' by Stephen Covey.",
    "image": "static/img/reading.webp"
},{
    "name": "Movies",
    "description": "I watch a lot of movies with my family. My favorite movies are the Indiana Jones series.",
    "image": "static/img/movies.jpeg"
},{
    "name": "Running",
    "description": "I Like going for a run, makes me feel relax. I am planning to run a marathon.",
    "image": "static/img/running.jpeg"
}]
educationArray = [
    {
        "school_name": "Monterrey Institute of Technology and Higher Education",
        "degree": "High School",
        "field_of_study": "",
        "start_year": "2017",
        "end_year": "2020",
        "grade": "90",
        "description": "Completed with honors."
    },
    {
        "school_name": "Monterrey Institute of Technology and Higher Education",
        "degree": "Bachelor's Degree",
        "field_of_study": "Computer Science",
        "start_year": "2020",
        "end_year": "2025",
        "grade": "92",
        "description": "Especializing in Software Engineering."
    }
]
work_experience = [
    {
        "job_title": "Software Engineer",
        "company_name": "Google",
        "start_date": "January 2021",
        "end_date": "Present",
        "location": "Mountain View, CA",
        "description": "Working on the Search team to improve the ranking algorithm."
    },
    {
        "job_title": "Intern",
        "company_name": "Microsoft",
        "start_date": "May 2020",
        "end_date": "August 2020",
        "location": "Redmond, WA",
        "description": "Worked on improving the performance of the Excel calculation engine."
    }
]

@app.route('/')
def index():
    return render_template('about.html', title='name')

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', hobbies=hobbiesArray)

@app.route('/places')
def places():
    return render_template('places.html', title="Places")

@app.route('/education')
def education():
    return render_template('education.html', title='Education', education=educationArray)

@app.route('/experience')
def experience():
    return render_template('experience.html', title='Work Experience', work_experience=work_experience)

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title='')

@app.route('/concept')
def concept():
    return render_template('concept.html', title="")

# API endpoints
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return "Invalid name", 400
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email", 400
    if not content:
        return "Invalid content", 400
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts':[
            model_to_dict(p) for p  in TimelinePost.select().order_by(-TimelinePost.created_at)
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    id = request.form['id']
    
    if (id == 'test'):
        TimelinePost.get(TimelinePost.name == id).delete_instance()
        return {
            'message': 'deleted'
        }

    try:
        post = TimelinePost.get_by_id(id)
        post.delete_instance()
        return {
            "message": 'deleted successfully'
        }
    except:
        return {
            "message": "An error happended while deleting the instance"
        }
