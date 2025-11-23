import requests

def test_app():
    response = requests.post('http://127.0.0.1:5000/users/new_user', json={
        'email': 'shawn5@example.com',
        'username': 'Shawn',
        'password': 'F00B@r2'
    })
    print(response.co)

if __name__ == "__main__":
    test_app()
