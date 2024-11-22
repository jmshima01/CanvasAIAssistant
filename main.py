from fastapi import FastAPI
from canvas import User
from ed import *
from openai import OpenAI
import re
import json

"""
--------
MarvinAI
--------
self-hosted AI assistant server for Canvas LMS and Ed-stem Discussion
@author James Shima
"""

app = FastAPI()

# User session instances
app.state.EdSession = None
app.state.CanvasSession = None
app.state.OpenAISession = None

# cached data
app.state.canvas_data = None
app.state.ed_data = None # only one per active course chat

# chosen ed course for questioning
app.state.ed_course_id = None
app.state.ed_course_name = None

@app.post("/login/canvas")
def canvas_login(canvas_token: str, canvas_url="https://elearning.mines.edu"):
    
    login = User(canvas_url, canvas_token)
    if not login.user or not login.canvas: # bad url/token
        return "Bad url or token"
    
    app.state.CanvasSession = login
    app.state.canvas_data = login.basic_user_scrape()

    return app.state.canvas_data

@app.post("/login/edstem")
def edstem_login(ed_token: str):
    try:
        ed = EdAPI()
        ed.login()
    except:
        return 1
    
    app.state.EdSession = ed
    return 0

@app.post("/login/openai")
def openai_login(api_key: str):
    try:
        login = OpenAI(api_key=api_key)
    except:
        return 1
    
    app.state.OpenAISession = login
    return 0

@app.get("/ed/list-courses")
def edstem_courses():
    if app.state.EdSession:
        app.state.ed_courses = get_ed_courses(app.state.EdSession)
        return app.state.ed_courses


@app.post("/ed/select-course")
def edstem_choose_thread(course_id: int):
    app.state.ed_course_id = course_id
    if app.state.EdSession:
        # only grabbing first 50 threads for relavance and token limitations...
        app.state.ed_data = get_threads(app.state.EdSession, app.state.EdSession.list_threads(course_id, limit=50), course_id, get_ed_courses(app.state.EdSession)[course_id])
        return app.state.ed_data
    return "No ed session" 


@app.get("/ask/canvas")
def ask_canvas(question: str):
    if app.state.CanvasSession and app.state.canvas_data:
        if app.state.OpenAISession:
            chat = app.state.OpenAISession.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a assistant for Canvas LMS \
                    Answer the student's question.\
                    Also, here is the student's basic Canvas Data for you to refer:\n{app.state.canvas_data}"},
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            return chat.choices[0].message.content
        else:
            return "Failed no OpenAI session found"
    else: return "Failed no Canvas session found"

    
@app.get("/ask/ed")
def ask_ed(question: str):
    if app.state.ed_data and app.state.EdSession:
        if app.state.OpenAISession:
            chat = app.state.OpenAISession.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a assistant for Ed-stem a Q&A. \
                    Answer the student's question.\
                    In addition, if the student requests you to post or ask something on ed for them, only return a single python dictionary with the \
                    fields...\ntitle: \"title_of_student_post\"content: \"post_content\" and only the dictionary. If the student doesn't provide you with the necessary data then infer the content and title they are asking for.\
                    Also if a post, add [MarvinAI-Beta] to the beginning of every post title and state you are an AI assistant for the student.\nLastly, here is the student's Canvas and Ed Data for you to refer:\n{app.state.ed_data}"},
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            response = chat.choices[0].message.content
            is_post = re.search("\{\s*(\"|\')title(\"|\')\s*:\s*(\"|\').*(\"|\')\s*,\s*(\"|\')content(\"|\')\s*:\s*(\"|\').*(\"|\')\s*,?\s*\}", response)
            if is_post is not None:
                try:
                    post = json.loads(str(is_post.group()))
                    title = post["title"]
                    content = post["content"]
                    post_on_ed(app.state.EdSession, app.state.ed_course_id, title, content)
                    return "posted your question on Ed!"
                except Exception as e:
                    print(f"Error posting question on ed request: {e}")
                    return f"Error posting question on ed request: {e}"
            else:
                return response
        else:
            return "No Open AI Session Found"
    else:
        return "No Ed data found"