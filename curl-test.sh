#!/bin/bash

#curl http://localhost:5000/api/timeline_post # Get the current posts
#curl -X POST http://localhost:5000/api/timeline_post -d 'name=test&email=test@email.com&content=Testing' # Add a testing post
#curl -X GET http://localhost:5000/api/timeline_post # Check if the post was added correctly
#curl -X DELETE http://localhost:5000/api/timeline_post -d 'id=test' # Delte the testing post
#curl -X GET http://localhost:5000/api/timeline_post # Finally, retrieve one more time all the post
# JSON data to send in the POST request
json='{
    "name": "test",
    "email": "test@example.com",
    "content": "This is a test post."
}'

# Send a POST request
echo "Sending POST request..."
post_response=$(curl -s --request POST http://localhost:5000/api/timeline_post'name=test&email=test@example.com&content=This is a test post.')

echo "POST Response: $post_response"

# Wait for a few seconds to ensure the POST request is processed
sleep 5

# Send a GET request
echo "Sending GET request..."
get_response=$(curl -s http://localhost:5000/api/timeline_post)

echo "GET Response: $get_response"

# Check if POST response is in the GET response
if [[ "$get_response" == *"$post_response"* ]]; then
  echo "The timeline post was successfully added."
else
  echo "The timeline post was not added."
fi
