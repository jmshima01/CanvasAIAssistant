#!/bin/env python3
from openai import OpenAI
import os, sys
from dotenv import load_dotenv
from edapi import EdAPI
from edapi.constants import ThreadType
from edapi.utils import new_document, parse_content
import re
import json
from requests.compat import urljoin

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

s = ""
with open("ed.txt", "r+") as f:
    s += f.read()
# with open("canvas.txt", "r+") as f:
#     s += f.read()

client = OpenAI(api_key=api_key)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"You are a assistant for Ed-stem a Q&A. \
         Answer the student's question.\
         In addition, if the student requests you to post or ask something on ed for them, only return a single python dictionary with the \
         fields...\ntitle: \"title_of_student_post\"content: \"post_content\" and only the dictionary. If the student doesn't provide you with the necessary data then infer the content and title they are asking for. \
         Also if a post, add [MarvinAI-Beta] to the beginning of every post title and state you are an AI assistant for the student. \
         If you are asked to post answer(s) to question(s) that either have no answer or you can add helpful insight or know the answer to, \
         then only return a single python dictionary with the fields of... question_id_str : your_answer_str stating you are [MarvinAI] an ai assistant. Lastly, here is the student's Canvas and Ed Data for you to refer:\n{s}"},
        {
            "role": "user",
            "content": "can you post answers to questions with no answer?"
        }
    ]
)

response = completion.choices[0].message.content
ed = EdAPI()
ed.login()
def post_on_ed(class_id, title, content, category=None):
    ed = EdAPI()
    ed.login()

    discussion_soup, document = new_document()
    p = discussion_soup.new_tag("paragraph")
    p.string = content
    document.append(p)

    ed.post_thread(class_id, {
    "type":  ThreadType.POST,
      "title": title,
      "category": "Cowboy Coding Era" if not category else category,
      "subcategory": "",
      "subsubcategory": "",
      "content": str(document),
      "is_pinned": False,
      "is_private": False,
      "is_anonymous": True,
      "is_megathread": False,
      "anonymous_comments": False,
    },)

def post_answer(ed: EdAPI, thread_id: int, content: str):
    discussion_soup, document = new_document()
    p = discussion_soup.new_tag("paragraph")
    p.string = content
    document.append(p)
    thread_url = urljoin("https://us.edstem.org/api/", f"threads/{thread_id}/comments")
    response = ed.session.post(thread_url, json={"comment": {"content":str(document),"is_annymous":True,"is_private":False,"type":"answer"}})
    if not response.ok:
        raise Exception(f"Failed to post comment in thread {thread_id}.", response.content)



is_post = re.search("\{\s*(\"|\')title(\"|\')\s*:\s*(\"|\').*(\"|\')\s*,\s*(\"|\')content(\"|\')\s*:\s*(\"|\').*(\"|\')\s*,?\s*\}", response)
is_answer = re.search("\{[\s\S]*\}", response)
if is_answer:
    try:
        # print(json.loads(str(is_answer.group())))
        for k,v in json.loads(str(is_answer.group())).items():
            post_answer(ed, int(k), v)
            print(f"posted {v} @ {k}")
            
    except Exception as e:
        raise Exception(f"failed {response} {e}")
    print(is_answer.group())
# if is_post is not None:
#     try:
#         post = json.loads(str(is_post.group()))
#         title = post["title"]
#         content = post["content"]

#         # post in ML:
#         post_on_ed(62781, title, content)
#     except Exception as e:
#         print(f"Error posting question on ed request: {e}")
#         sys.exit(1)
# else:
print("==================")
print(response)
