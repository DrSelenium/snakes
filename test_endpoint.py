import requests

# Read the test SVG
with open('test_board.svg', 'r') as f:
    svg_content = f.read()

# Send POST request to /slpu endpoint
url = 'http://127.0.0.1:5000/slpu'
headers = {'Content-Type': 'image/svg+xml'}

response = requests.post(url, data=svg_content, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Response: {response.text}")
