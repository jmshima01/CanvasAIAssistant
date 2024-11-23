#!/bin/env python3
"""
@author James Shima
"""
from requests.compat import urljoin
from edapi import EdAPI
from edapi.constants import ThreadType
from edapi.utils import new_document, parse_content
from pathlib import Path
from dotenv import load_dotenv

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
        
def post_on_ed(ed, class_id, title, content, category=None):
    
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
      "is_anonymous": True,
      "is_megathread": False,
      "anonymous_comments": False,
    },)


def get_ed_courses(ed: EdAPI):
    info = ed.get_user_info()
    courses = {}
    for c in info["courses"]:
        c = c["course"]
        if c["status"] == "active" and c["year"] == "2024" and c["session"] == "Fall":
            courses[int(c["id"])] = c["name"]  

    return courses

def get_threads(ed: EdAPI, threads, id, name):
    s = f"Ed-stem Q&A for {name} (id={id}):\n"
    
    for t in threads:
        s+="-------------------------\n"
        
        no_newline = " ".join(t["document"].split())
        
        s+=f'Question id={t["id"]}: ({t["category"]}) {t["title"]} @ {t["created_at"]}:\n\"{no_newline}\"\n\n'
        
        if ed.get_thread(t["id"])["answers"]:
            for i in ed.get_thread(t["id"])["answers"]:
                no_newline = " ".join(i["document"].split())
                s+= f'Answer: \"{no_newline}\"\n\n'
                if i["comments"]:
                    s+="Comments:\n"
                    def comments(l,j,s):
                        tabs = "\t"*j+"| "
                        no_newline = " ".join(l["document"].split())
                        
                        s[0]+= f'{tabs}\"{no_newline}\"\n'
                        if not l["comments"]:
                            return
                        comments(l["comments"][0],j+1,s)
                    for c in i["comments"]:
                        g = [s]
                        comments(c,0,g)
                        s = g[0]
                    s+="\n"
        
        elif ed.get_thread(t["id"])["comments"]:
            s+="Comments:\n"
            def comments(l,j,s):
                tabs = "\t"*j+"| "
                no_newline = " ".join(l["document"].split())
                
                s[0]+=f'{tabs}\"{no_newline}\"\n'
                if not l["comments"]:
                    return
                comments(l["comments"][0],j+1,s)
            for c in ed.get_thread(t["id"])["comments"]:
                l = [s]
                comments(c,0,l)
                s = l[0]
            s+="\n"        
        else:
            s+="Answer: None\n\n"
    
    return s




def save_api_key(api_key: str, env_file: str = ".env") -> bool:
    
    try:
        env_path = Path(env_file)
        
        # If .env exists, read existing content
        if env_path.exists():
            with open(env_path, 'r') as file:
                lines = file.readlines()
            
            # Check if API_KEY already exists
            api_key_exists = False
            for i, line in enumerate(lines):
                if line.startswith('ED_API_TOKEN='):
                    lines[i] = f'ED_API_TOKEN=\"{api_key}\"\n'
                    api_key_exists = True
                    break
            
            # If API_KEY not found, append it
            if not api_key_exists:
                lines.append(f'\nED_API_TOKEN=\"{api_key}\"\n')
                
            # Write back all lines
            with open(env_path, 'w') as file:
                file.writelines(lines)
        
        else:
            # Create new .env file with API key
            with open(env_path, 'w') as file:
                file.write(f'ED_API_TOKEN=\"{api_key}\"\n')
        
        # Reload environment variables
        load_dotenv(override=True)
        return True
        
    except Exception as e:
        print(f"Error saving API key: {e}")
        return False

def post_comment(ed: EdAPI, thread_id: int, content: str):
    discussion_soup, document = new_document()
    p = discussion_soup.new_tag("paragraph")
    p.string = content
    document.append(p)
    thread_url = urljoin("https://us.edstem.org/api/", f"threads/{thread_id}/comments")
    response = ed.session.post(thread_url, json={"comment": {"content":str(document),"is_annymous":True,"is_private":False,"type":"comment"}})
    if not response.ok:
        raise Exception(f"Failed to post comment in thread {thread_id}.", response.content)

def post_answer(ed: EdAPI, thread_id: int, content: str):
    discussion_soup, document = new_document()
    p = discussion_soup.new_tag("paragraph")
    p.string = content
    document.append(p)
    thread_url = urljoin("https://us.edstem.org/api/", f"threads/{thread_id}/comments")
    response = ed.session.post(thread_url, json={"comment": {"content":str(document),"is_annymous":True,"is_private":False,"type":"answer"}})
    if not response.ok:
        raise Exception(f"Failed to post comment in thread {thread_id}.", response.content)

if __name__ == "__main__":
    
    ed = EdAPI()
    ed.login()
    user_info = ed.get_user_info()
    
    post_answer(ed, 5764373, "test")
    # student_name(user_info)

    # ml ed discussion
    # threads = ed.list_threads(62781)
    # print_treads(ed,threads)
    # user_info = ed.get_user_info()
    # print(get_threads(ed,ed.list_threads(62781),62781))