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
        
        print(f'({t["category"]}) {t["title"]} @ {t["created_at"]}:\n\"{no_newline}\"\n')
        
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
                    comments(i["comments"][0],0)
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
            comments(ed.get_thread(t["id"])["comments"][0],0)
            print()        
        else:
            print("Answer: None\n")
        
def post_on_ed():
    pass
    # discussion_soup, document = new_document()
    # dis_a_paragraph = discussion_soup.new_tag("paragraph")
    # dis_a_paragraph.string = f"this is a test :) "
    # document.append(dis_a_paragraph)

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

    # resp = ed.session.post(urljoin("https://us.edstem.org/api/", f"threads/{5699131}/pin"))
    # print(resp)

if __name__ == "__main__":
    ed = EdAPI()
    ed.login()
    user_info = ed.get_user_info()
    
    student_name(user_info)

    # ml
    threads = ed.list_threads(62781)
    print_treads(ed,threads)