import requests

def test_app():
    response = requests.post('http://127.0.0.1:5000/users/get_user', json={'id': '7b12eb00-55e7-4e05-b4af-1798a51dea4c'})
    print(response.text)

if __name__ == "__main__":
    test_app()
