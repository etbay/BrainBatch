import requests

def test_app():
    response = requests.post('http://127.0.0.1:5000/groups/remove_moderator', json={
        'group_id': 'd42d18f5-3891-4072-b73e-c2f0934932de',
        'user_id': '68512da7-c760-4ab6-8491-72819e02adf7'
    })
    print(response.text)

if __name__ == "__main__":
    test_app()
