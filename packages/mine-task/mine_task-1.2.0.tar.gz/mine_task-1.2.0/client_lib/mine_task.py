import os
import json
import requests

class ServerResponse:
    def __init__(self, status, detail=None):
        self.status = status
        self.detail = detail

class Task:
    def __init__(self, title, content, everyday=True):
        self.title = title
        self.content = content
        self.everyday = everyday

    def to_dict(self):
        return {
            "type": "normal",
            "title": self.title,
            "command": self.content,
            "everyday": True if self.everyday else False
        }

class TaskManager:
    def __init__(self, session):
        self.session = session

    def status(self, detail=False):
        resp = requests.get(
            f"{self.session.api_url}/tasks",
            headers={"x-api-key": self.session.api_key}
        )
        if resp.status_code == 200:
            tasks = resp.json().get("tasks", [])
            if not tasks:
                print("No tasks found.")
                return
            if not detail:
                for t in tasks:
                    print(f"[{t.get('index')}] {t.get('title')} | Running: {t.get('running')}")
            else:
                for t in tasks:
                    print("="*40)
                    print(f"Index:        {t.get('index')}")
                    print(f"Title:        {t.get('title')}")
                    print(f"Content:      {t.get('command')}")
                    print(f"Email:        {t.get('email')}")
                    print(f"Cron:         {t.get('cron')}")
                    print(f"Everyday:     {t.get('everyday')}")
                    print(f"Running:      {t.get('running')}")
                    print(f"Next Run:     {t.get('next_run_time')}")
                    print(f"Job ID:       {t.get('job_id')}")
                print("="*40)
        else:
            print(f"Error: {resp.text}")

    def rm(self, name, is_all=False):
        if isinstance(name, int):
            data = {"index": name}
        elif isinstance(name, list):
            data = {"titles": name}
        else:
            data = {"title": name, "is_all": is_all}
        requests.delete(
            f"{self.session.api_url}/tasks",
            headers={"x-api-key": self.session.api_key},
            json=data
        )
        # 不返回任何内容

    def modify(self, name, new_title=None, new_content=None, new_time=None, everyday=None):
        data = {}
        if isinstance(name, int):
            data["index"] = name
        else:
            data["title"] = name
        if new_title is not None:
            data["new_title"] = new_title
        if new_content is not None:
            data["new_content"] = new_content
        if new_time is not None:
            data["new_time"] = new_time
        if everyday is not None:
            data["everyday"] = everyday
        resp = requests.put(
            f"{self.session.api_url}/tasks",
            headers={"x-api-key": self.session.api_key},
            json=data
        )
        return resp.json().get("msg", "Task updated") if resp.status_code == 200 else {"error": resp.text}

class Session:
    def __init__(self, api_url):
        self.api_url = api_url.rstrip('/')
        self.api_key = None
        self.connected = False
        self.status = None
        self.task = TaskManager(self)

    def login_server(self, key):
        self.api_key = key
        try:
            resp = requests.get(f"{self.api_url}/tasks", headers={"x-api-key": key})
            if resp.status_code == 200:
                self.connected = True
                self.status = 'ok'
                return self
            elif resp.status_code == 401:
                self.connected = False
                self.status = 'fail'
                return self
            else:
                self.connected = False
                self.status = 'fail'
                return self
        except Exception as e:
            self.connected = False
            self.status = 'fail'
            return self

    def sub(self, task: Task, email=None):
        if not self.connected or not self.api_key:
            return 'Not connected.'
        data = task.to_dict()
        if email:
            data["email"] = email
        else:
            data["email"] = "test@test.com"
        if not task.everyday:
            data["cron"] = "0 8 * * *"
        resp = requests.post(f"{self.api_url}/tasks", headers={"x-api-key": self.api_key}, json=data)
        if resp.status_code == 200:
            return 'Business creation completed'
        else:
            return resp.text

    def create_user(self, obtain="terminal"):
        resp = requests.post(f"{self.api_url}/register")
        if resp.status_code == 200 and "api_key" in resp.json():
            api_key = resp.json()["api_key"]
            if obtain == "terminal":
                return f"your key: {api_key}"
            elif obtain == "json":
                user_home = os.path.expanduser("~")
                json_path = os.path.join(user_home, "api_key.json")
                with open(json_path, "w") as f:
                    json.dump({"api_key": api_key}, f)
                return f"your key is in '{json_path}'"
            else:
                raise ValueError("obtain must be 'terminal' or 'json'")
        else:
            raise Exception(f"Failed to register user: {resp.text}")

    def destroy_user(self, key):
        resp = requests.post(f"{self.api_url}/unregister", headers={"x-api-key": key})
        if resp.status_code == 200:
            return resp.json().get("msg", "User unregistered.")
        else:
            return resp.text

def connect_session(api_url="http://101.132.187.196:5066"):
    return Session(api_url)

def create_normal_task(task_title, task_content, everyday=True):
    return Task(task_title, task_content, everyday) 