#!/bin/env python3
"""
@author James Shima
"""
from requests.compat import urljoin
from edapi import EdAPI
from edapi.constants import ThreadType
from edapi.utils import new_document, parse_content


def student_name(user_info):
    user = user_info['user']
    print(f"STUDENT NAME: {user['name']}\n")


def course_ids(user_info):
    return [(d["course"]["id"],d["course"]["name"]) for d in user_info["courses"] if d["course"]["year"]=="2024"]


def print_treads(ed, threads):
    for t in threads:
        print("-------------------------")
        no_newline = " ".join(t["document"].split())
        
        print(f'Question: ({t["category"]}) {t["title"]} @ {t["created_at"]}:\n\"{no_newline}\"\n')
        
        if ed.get_thread(t["id"])["answers"]:
            for i in ed.get_thread(t["id"])["answers"]:
                no_newline = " ".join(i["document"].split())
                print(f'Answer: \"{no_newline}\"\n')
                if i["comments"]:
                    print("Comments:")
                    def comments(l,j):
                        tabs = "\t"*j+"| "
                        no_newline = " ".join(l["document"].split())
                        print(f'{tabs}\"{no_newline}\"')
                        if not l["comments"]:
                            return
                        comments(l["comments"][0],j+1)
                    for c in i["comments"]:
                        comments(c,0)
                    
                    print()
        
        elif ed.get_thread(t["id"])["comments"]:
            print("Comments:")
            def comments(l,j):
                tabs = "\t"*j+"| "
                no_newline = " ".join(l["document"].split())
                print(f'{tabs}\"{no_newline}\"')
                if not l["comments"]:
                    return
                comments(l["comments"][0],j+1)
            for c in ed.get_thread(t["id"])["comments"]:
                comments(c,0)
            print()        
        else:
            print("Answer: None\n")
        
def post_on_ed(class_id, title, content, category=None):
    
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

if __name__ == "__main__":
    ed = EdAPI()
    ed.login()
    user_info = ed.get_user_info()
    
    student_name(user_info)

    # ml ed discussion
    threads = ed.list_threads(62781)
    print_treads(ed,threads)