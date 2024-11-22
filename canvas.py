#!/bin/env python3
"""
@author James Shima
"""
from canvasapi import Canvas
import os
from dotenv import load_dotenv
import requests
import sys
import traceback
from datetime import datetime, timezone
import re

def get_canvas_cred():
    load_dotenv()
    url = os.getenv("CANVAS_API_URL")
    key = os.getenv("CANVAS_API_KEY")
    return url, key

class User:
    def __init__(self, url, key):
        self._canvas = None
        try:
            self._canvas = Canvas(url, key)
        except Exception as e:
            print(f"Unable to load Canvas with {url} and {key}",e)
        
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
            return None

        if resp.status_code != 200:
            print(f"Status Code: {resp.status_code} Error unable to get canvas user id. Make sure api key and url are correct \
                  (i.e. API_CANVAS_URL = https://elearning.mines.edu) without the /api/v1/...\n Your url: {url}")
            return None

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
    
    """
    returns basic user data scrape as a string to pass to AI prompt
    """
    def basic_user_scrape(self):
        s = ""
        s+= "COURSES:\n"
        for course in self.course_list():
            s+= f"- {course.name}\n"

        s+= "\nDUE ASSIGNMENTS:\n"
        due_assignments = {}
        current_time = datetime.now(timezone.utc)
        for course in self.course_list():
            assignments = course.get_assignments()
            for assignment in assignments:
                # Check if the assignment has a due date and is still due
                try:
                    if assignment.due_at:
                        due_date = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                        if due_date > current_time:
                            # Store assignment details
                            if course.name not in due_assignments:
                                due_assignments[course.name] = []
                            
                            due_assignments[course.name].append({
                                "name": assignment.name,
                                "description": assignment.description,
                                "due_at": assignment.due_at,
                                "points_possible": assignment.points_possible,
                                "submission_types": assignment.submission_types,
                                "html_url": assignment.html_url,
                            })
                except: pass

        for course, assignments in due_assignments.items():
            s += f"Course: {course}\n"
            for assignment in assignments:
                s += f"    Assignment for {course}: {assignment['name']}\n"
                s += f"    Due At: {assignment['due_at']}\n"
                s += f"    Points: {assignment['points_possible']}\n"
                s += f"    Submission Types: {', '.join(assignment['submission_types'])}\n"
                s += f"    Description: {assignment['description']}\n"
                s += f"    URL: {assignment['html_url']}\n\n"
        
        
        s+= "CURRENT GRADES:\n"

        for course in self.user.get_enrollments(type="StudentEnrollment"):
            try:
                grade = course.grades
                s += f'{self.canvas.get_course(course.course_id).name} {grade["current_score"]} {grade["current_grade"]}\n'       
            except Exception as e:
                pass
        return s
        

"""
Test scraping locally
"""
if __name__ == "__main__":
    API_URL, API_KEY = get_canvas_cred()
    user = User(API_URL, API_KEY)

    # Get all courses
    print("COURSES:")
    for course in user.course_list():
        print(f"- {course.name}")

    print("\nDUE ASSIGNMENTS:")
    due_assignments = {}
    current_time = datetime.now(timezone.utc)
    for course in user.course_list():
        assignments = course.get_assignments()
        for assignment in assignments:
            # Check if the assignment has a due date and is still due
            try:
                if assignment.due_at:
                    due_date = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    if due_date > current_time:
                        # Store assignment details
                        if course.name not in due_assignments:
                            due_assignments[course.name] = []
                        
                        due_assignments[course.name].append({
                            "name": assignment.name,
                            "description": assignment.description,
                            "due_at": assignment.due_at,
                            "points_possible": assignment.points_possible,
                            "submission_types": assignment.submission_types,
                            "html_url": assignment.html_url,
                        })
            except: pass

    for course, assignments in due_assignments.items():
        print(f"\nCourse: {course}")
        for assignment in assignments:
            print(f"    Assignment for {course}: {assignment['name']}")
            print(f"    Due At: {assignment['due_at']}")
            print(f"    Points: {assignment['points_possible']}")
            print(f"    Submission Types: {', '.join(assignment['submission_types'])}")
            print(f"    Description: {assignment['description']}")
            print(f"    URL: {assignment['html_url']}\n")
    
    # download all pdfs if want to...
    # wanted_course_ids = [67414,69225,69213]
    # want = re.compile(".*[sS]yllabus.*|.*\.pdf")
    # for i in wanted_course_ids:
    #     files = user.canvas.get_course(i).get_files()
    #     try:
    #         for f in files:
    #             if want.match(str(f)):
    #                 f.download(f"files/{f}")
    #     except Exception as e:
    #         pass
    
    print("CURRENT GRADES:")

    for course in user.user.get_enrollments(type="StudentEnrollment"):
        try:
            grade = course.grades
            print(user.canvas.get_course(course.course_id).name, grade["current_score"],grade["current_grade"])      
        except Exception as e:
            pass
    
    # for course in user.course_list():
    #     print(f"\nPAGES for {course.name}:")
    #     try:
    #         for page in course.get_pages():
    #             page_html = course.get_page(page.url).body
    #             print(page_html)
        
    #     except: print("None")