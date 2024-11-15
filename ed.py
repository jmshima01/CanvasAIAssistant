#!/bin/env python3
"""
@author James Shima
11/12/24
"""



from requests.compat import urljoin
from edapi import EdAPI
from edapi.constants import ThreadType
from edapi.utils import new_document, parse_content
ed = EdAPI()



ed.login()

user_info = ed.get_user_info()
# print(user_info)
print("======================")
course_ids = [(d["course"]["id"],d["course"]["name"]) for d in user_info["courses"] if d["course"]["status"]=="active"]

user = user_info['user']
print(f"Hello {user['name']}!")
print(course_ids)
threads = ed.list_threads(62886)

# print(ed.get_thread(5699131))
# print(threads)
discussion_soup, document = new_document()
dis_a_paragraph = discussion_soup.new_tag("paragraph")
dis_a_paragraph.string = f"this is a test :) "
document.append(dis_a_paragraph)

# ed.post_thread(62781, {
# "type":  ThreadType.ANNOUNCEMENT,
#   "title": "This is an AI Agent: Testing",
#   "category": "THIS IS AI",
#   "subcategory": "HACKED",
#   "subsubcategory": "uwu",
#   "content": str(document),
#   "is_pinned": False,
#   "is_private": True,
#   "is_anonymous": True,
#   "is_megathread": True,
#   "anonymous_comments": False,
# },)

resp = ed.session.post(urljoin("https://us.edstem.org/api/", f"threads/{5699131}/pin"))
print(resp)