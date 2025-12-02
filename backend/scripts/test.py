import requests


def test_app():
    response = requests.post('http://127.0.0.1:5000/users/login', json={
        'email': 'anthony@example.com',
        'password': 'F00B@r!'
    })

    print(response.json())

    response = requests.post('http://127.0.0.1:5000/users/get_user', json={
        'id': response.json()["data"]["id"]
    })

    print(response)

    # response = requests.get('http://127.0.0.1:5000/users/reset_password?email=anthony@example.com')

if __name__ == "__main__":
    test_app()
