import json
import requests

def show_response(response, n):
    print(f"Test {n}" )
    print(f"{response.request}")
    print(f"STATUS CODE {response.status_code}")
    print(f"JSON CONTENT:")
    print(json.dumps(response.json(), indent=4))

def test_home(n):
    response = requests.get(url="http://localhost:5000/")
    show_response(response, n)

def test_all_rides(n):
    response = requests.get(url="http://localhost:5000/rides")
    show_response(response, n)

def test_get_ride(ride_id: str, n):
    response = requests.get(url=f"http://localhost:/rides/{ride_id}")
    show_response(response, n)

if __name__ == "__main__":
    test_home(1)
    test_all_rides(2)
