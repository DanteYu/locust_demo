from locust import HttpLocust, TaskSet, task, between

class UserTask(TaskSet):

    @task
    def tc_index(self):
        self.client.get("/")

class UserOne(HttpLocust):
    task_set = UserTask
    # 被挑选执行的权重，数值越大，执行频率越高
    weight = 1
    # 设置 Locust 多少秒后超时，如果为 None ,则不会超时
    stop_timeout = 5
    wait_time = between(1, 3)
    host = "https://www.baidu.com"

class UserTwo(HttpLocust):
    weight = 2
    task_set = UserTask
    stop_timeout = 5
    wait_time = between(1, 3)
    host = "https://www.baidu.com"