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
    "name": "Coding"
},{
    "name": "Hang out with my family and friends"
},{
    "name": "Reading"
},{
    "name": "Movies"
},{
    "name": "Excercise"
},{
    "name": "Watching the sky"
},{
    "name": "Playing the guitar"
},{
    "name": "Music"
}
]
educationArray = [
    {
        "school_name": "Universidad Nacional Autónoma de México",
        "degree": "Electrical and electronics",
        "field_of_study": "audio",
        "start_year": "2019",
        "end_year": "2024",
        "description": "Minor in audio",
        "image": "../static/img/unam.jpeg"
    }
]
work_experience = [
    {
        "job_title": "Frontend developer",
        "company_name": "Roatech",
        "start_date": "May 2022",
        "end_date": "June 2023",
        "location": "Mexico City, Mexico",
        "description": "Created multiple microservices for Bradescard bank. I used Power Automate to optimize invoice data extraction time by over 200%."
    }
]

@app.route('/')
def index():
    return render_template('index.html', title='name', work_experience=work_experience, education=educationArray, hobbies=hobbiesArray)

# API endpoints
@app.route('/api/timeline_post/add', methods=['POST'])
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
