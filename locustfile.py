from locust import HttpLocust, TaskSet
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

def login(l):
    l.client.post("/login", {"username":"ellen_key", "password":"education"})

def logout(l):
    l.client.post("/logout", {"username":"ellen_key", "password":"education"})

def index(l):
    l.client.get("/")

class UserBehavior(TaskSet):
    tasks = {index: 2}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
