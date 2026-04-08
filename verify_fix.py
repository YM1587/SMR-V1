import http.client
import json

def test_endpoint(path):
    conn = http.client.HTTPConnection("localhost", 8000)
    conn.request("POST", path, body=json.dumps({}), headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    print(f"Path: {path} -> Status: {response.status}")
    if response.status == 307:
        print(f"  Redirect location: {response.getheader('Location')}")
    conn.close()

print("Testing milk production endpoint...")
test_endpoint("/production/milk/")

print("\nTesting weight production endpoint...")
test_endpoint("/production/weight/")

print("\nTesting breeding production endpoint...")
test_endpoint("/production/breeding/")

print("\nTesting pen feed log endpoint...")
test_endpoint("/feed/pen/")

print("\nTesting individual feed log endpoint...")
test_endpoint("/feed/individual/")
