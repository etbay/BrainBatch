import requests
import os
import json


def test_app():
    """response = requests.post("http://127.0.0.1:5000/groups/add_chat_area", json={
        "chat_area_name": "General",
        "group_id": "cf705328-73b6-44b9-b1b1-04b613daf9a6"
    })"""

    json_data = {
        "chat_area_name": "General",
        "group_id": "cf705328-73b6-44b9-b1b1-04b613daf9a6",
        "sender_id": "f4776525-87d8-4713-a8f4-e71abcc8d973",
        "message": "Basic Attachment"
    }

    file = "HEAVY.png"

    with open(file, 'rb') as file:
        response = requests.post("http://127.0.0.1:5000/groups/send_message",
                                files={"file": file},
                                data=json_data)

    """response = requests.post("http://127.0.0.1:5000/groups/delete_message", json={
        "chat_area_name": "General",
        "group_id": "cf705328-73b6-44b9-b1b1-04b613daf9a6",
        "message_index": 0
    })"""

    """response = requests.post("http://127.0.0.1:5000/groups/remove_chat_area", json={
        "chat_area_name": "General",
        "group_id": "cf705328-73b6-44b9-b1b1-04b613daf9a6"
    })"""

    print(response.content)


if __name__ == "__main__":
    test_app()
