
import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert  '<h2 class="text-3xl font-bold pt-5" id="aboutme">About me</h2>' in html

    def test_timeline(self):
        getResponse = self.client.get('/api/timeline_post')
        assert getResponse.status_code == 200
        assert getResponse.is_json
        json = getResponse.get_json()
        assert 'timeline_posts' in json
        assert len(json['timeline_posts']) == 0

        postResponse = self.client.post('/api/timeline_post/add', data={
            'name': 'Test Name',
            'email': 'thisisatest@test.com',
            'content': 'test test test test'
        })
        assert postResponse.status_code == 200

        getResponse = self.client.get('/api/timeline_post')
        json = getResponse.get_json()
        first_timeline_post = json['timeline_posts'][0]
        first_timeline_post['name'] = 'Test Name'
        first_timeline_post['email'] = 'thisisatest@test.com'
        first_timeline_post['content'] = 'test test test test'

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post/add", data={"email": "john@example.com", "content": "Hello world I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request missing content
        response = self.client.post("/api/timeline_post/add", data={"name": "John Doe", "email": "john@example.com"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with invalid email format
        response = self.client.post("/api/timeline_post/add", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
