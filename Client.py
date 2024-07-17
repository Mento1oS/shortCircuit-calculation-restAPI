from fastapi import FastAPI

import requests

app = FastAPI()


def post_request():
    content = requests.post(
        url="http://127.0.0.1:8080/api/scheme",
        data=open("input.xml", "r"),
        headers={
            'Content-Type': 'application/xml'
        }
    )
    print(content.content.__str__())


def get_request(scheme_id, sc_place):
    content = requests.get(
        url=f"http://127.0.0.1:8080/api/scheme/{scheme_id}/?sc_place={sc_place}",
        headers={
            'Content-Type': 'application/json'
        }
    )
    print(content.content.__str__())


def put_request(scheme_id):
    content = requests.put(
        url=f"http://127.0.0.1:8080/api/scheme/{scheme_id}",
        data=open("input_on_put.xml", "r"),
        headers={
            'Content-Type': 'application/xml'
        }
    )
    print(content.content.__str__())


def delete_request(scheme_id):
    content = requests.delete(
        url=f"http://127.0.0.1:8080/api/scheme/{scheme_id}",
        headers={
            'Content-type': 'application/json'
        }
    )
    print(content.content.__str__())

# post_request()

get_request(2,2)
#
# put_request(2)
#
# delete_request(6)
