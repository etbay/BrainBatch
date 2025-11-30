import requests


def test_app():
    """files = {'file': ('example.txt', open('example.txt', 'rb'), 'text/plain')}
    response = requests.post('http://127.0.0.1:5000/uploads/upload_file', files=files)

    if response:
        print(response.json())
    else:
        print("No response")"""
    
    response = requests.get('http://127.0.0.1:5000/uploads/get_file?id=7d3c3ab6-458b-4345-afbf-00b5ba859230')
    print(response.url)

if __name__ == "__main__":
    test_app()
