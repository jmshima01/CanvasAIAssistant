#!/bin/env python3
from openai import OpenAI
import os
from dotenv import load_dotenv
import tiktoken

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
        {"role": "system", "content": f"You are a assistant for Canvas LMS and Ed-stem a Q&A. Answer the student question.\nData:\n{s}"},
        {
            "role": "user",
            "content": "is there any useful info for hw3 on ed?"
        }
    ]
)

print(completion.choices[0].message)