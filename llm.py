#!/bin/env python3
from openai import OpenAI
import os, sys
from dotenv import load_dotenv
from edapi import EdAPI
from edapi.constants import ThreadType
from edapi.utils import new_document, parse_content
import re
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

s = ""
with open("ed.txt", "r+") as f:
    s += f.read()
with open("canvas.txt", "r+") as f:
    s += f.read()

client = OpenAI(api_key=api_key)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"You are a assistant for Canvas LMS and Ed-stem a Q&A. \
         Answer the student's question.\
         In addition, if the student requests you to post or ask something on ed for them, only return a single python dictionary with the \
         fields...\ntitle: \"title_of_student_post\"content: \"post_content\" and only the dictionary. If the student doesn't provide you with the necessary data then infer the content and title they are asking for.\
         Also if a post, add [MarvinAI-Beta] to the beginning of every post title and state you are an AI assistant for the student.\nLastly, here is the student's Canvas and Ed Data for you to refer:\n{s}"},
        {
            "role": "user",
            "content": "what is my average grade right now?"
        }
    ]
)

response = completion.choices[0].message.content



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
      "category": "[MARVIN-AI-BETA]" if not category else category,
      "subcategory": "",
      "subsubcategory": "",
      "content": str(document),
      "is_pinned": False,
      "is_private": False,
      "is_anonymous": False,
      "is_megathread": False,
      "anonymous_comments": False,
    },)

is_post = re.search("\{\s*(\"|\')title(\"|\')\s*:\s*(\"|\').*(\"|\')\s*,\s*(\"|\')content(\"|\')\s*:\s*(\"|\').*(\"|\')\s*,?\s*\}", response)
if is_post is not None:
    try:
        post = json.loads(str(is_post.group()))
        title = post["title"]
        content = post["content"]
        post_on_ed(62781, title, content)
    except Exception as e:
        print(f"Error handling ed post request: {e}")
        sys.exit(1)
else:
    print(response)