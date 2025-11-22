import requests

def test_app():
    response = requests.post('http://127.0.0.1:5000/groups/new_group', json={
        'group_name': 'Foobar',
        'creator_id': '400f395c-fc85-45d4-a884-883d33d18291'
    })
    print(response.text)

if __name__ == "__main__":
    test_app()
