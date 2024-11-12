#!/bin/env python3

"""
@author James Shima
11/12/24
"""
from canvasapi import Canvas
import os
from dotenv import load_dotenv
import requests
import sys
import traceback

def get_canvas_cred():
    load_dotenv()
    url = os.getenv("CANVAS_API_URL")
    key = os.getenv("CANVAS_API_KEY")
    return url, key

class User:
    def __init__(self, url, key):
        self._canvas = Canvas(url, key)
        self._user = self._load_user(url, key)

    """
    Get user id and return user obj
    """
    def _load_user(self, url, key):
        try:
            params = {"access_token" : key}
            resp = requests.get(f"{url}/api/v1/users/self", params=params)
        except Exception as e:
            print(f"Error requesting canvas id: {e}\n{traceback.format_exc()}")
            sys.exit(1)

        if resp.status_code != 200:
            print(f"Status Code: {resp.status_code} Error unable to get canvas user id. Make sure api key and url are correct \
                  (i.e. API_CANVAS_URL = https://elearning.mines.edu) without the /api/v1/...\n Your url: {url}")
            sys.exit(1)

        user_data = resp.json()
        return self._canvas.get_user(user_data["id"])

    @property
    def user(self):
        return self._user
    
    @property
    def canvas(self):
        return self._canvas

    def course_list(self):
        return [c for c in self._user.get_courses() if hasattr(c,"name")]


def main():
    API_URL, API_KEY = get_canvas_cred()
    
    user = User(API_URL, API_KEY)
    
    # for i in user.course_list():
    #     print(i)

    print(list(user.user.get_calendar_events_for_user()))
    for i in user.user.get_files():
        print(i)

if __name__ == "__main__":
    main()