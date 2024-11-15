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
from datetime import datetime, timezone

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
        return [self._canvas.get_course(i.course_id) for i in list(self._user.get_enrollments(type='StudentEnrollment'))]
    
    def course_ids(self):
        return [i.course_id for i in list(self._user.get_enrollments(type='StudentEnrollment'))]

    def enrollments(self):
        return list(self._user.get_enrollments())

    def user_files(self):
        return list(self._user.get_files())

    def calendar_events(self):
        return list(self._user.get_calendar_events_for_user())
    

def main():
    API_URL, API_KEY = get_canvas_cred()
    user = User(API_URL, API_KEY)

    # Get all courses
    # print("User's Courses:")
    # for course in user.course_list():
    #     print(f"- {course.name}")

    # due_assignments = {}
    # current_time = datetime.now(timezone.utc)
    # for course in user.course_list():
    #     assignments = course.get_assignments()
    #     for assignment in assignments:
    #         # Check if the assignment has a due date and is still due
    #         try:
    #             if assignment.due_at:
    #                 due_date = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    #                 if due_date > current_time:
    #                     # Store assignment details
    #                     if course.name not in due_assignments:
    #                         due_assignments[course.name] = []
                        
    #                     due_assignments[course.name].append({
    #                         "name": assignment.name,
    #                         "description": assignment.description,
    #                         "due_at": assignment.due_at,
    #                         "points_possible": assignment.points_possible,
    #                         "submission_types": assignment.submission_types,
    #                         "html_url": assignment.html_url,
    #                     })
    #         except:
    #             pass
    # print("User's Assignments:")
    # for course, assignments in due_assignments.items():
    #     print(f"\nCourse: {course}")
    #     for assignment in assignments:
    #         print(f"  - Assignment for {course}: {assignment['name']}")
    #         print(f"    Due At: {assignment['due_at']}")
    #         print(f"    Points: {assignment['points_possible']}")
    #         print(f"    Submission Types: {', '.join(assignment['submission_types'])}")
    #         print(f"    Description: {assignment['description']}")
    #         print(f"    URL: {assignment['html_url']}\n")
    # print("-----------------------------")
    
    for i in user.course_ids():
        files = user.canvas.get_course(i).get_files()
        try:
            for f in files:
                print(f.download())
        except Exception as e:
            print(e)



if __name__ == "__main__":
    main()