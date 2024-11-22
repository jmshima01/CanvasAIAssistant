from fastapi import FastAPI
from canvas import User
from ed import *
from openai import OpenAI

"""
--------
MarvinAI
--------
self-hosted AI assistant server for Canvas LMS and Ed-stem Discussion
@author James Shima
"""

app = FastAPI()

# glob tokens for user
user_canvas_token = None
user_ed_token = None
user_openai_token = None

# User session instances
app.state.EdSession = None
app.state.CanvasSession = None
app.state.OpenAISession = None

@app.post("/login/canvas")
def canvas_login(canvas_token: str, canvas_url="https://elearning.mines.edu"):
    
    login = User(canvas_url, canvas_token)
    if not login.user or not login.canvas: # bad url/token
        return 1
    
    app.state.CanvasSession = login

    return 0

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

@app.get("/ask/canvas")
def ask_canvas(question: str):
    if app.state.CanvasSession is not None:
        user_data = app.state.CanvasSession.basic_user_scrape()
        if app.state.OpenAISession is not None:
            chat = app.state.OpenAISession.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a assistant for Canvas LMS \
                    Answer the student's question.\
                    Also, here is the student's basic Canvas Data for you to refer:\n{user_data}"},
                    {
                        "role": "user",
                        "content": "what is my average grade right now"
                    }
                ]
            )

            response = chat.choices[0].message.content
            return response
        else:
            return "Failed no OpenAI session found"
    else: return "Failed no Canvas session found"

    
@app.get("/ask/ed")
def ask_ed(thread_id: int, question: str):
    return question
