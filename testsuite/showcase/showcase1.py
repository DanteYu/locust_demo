from locust import HttpLocust, TaskSet, task, between


class UserBehaviourGet(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("I am the on_start")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("I am the on_stop")

    @task(2)
    def test_para(self):
        parameters = {"City": "Chengdu", "Location": "SoftwarePark"}
        # 通过client属性来使用Python requests库的所有方法
        r = self.client.get("/get", params=parameters)
        assert r.status_code == 200

    @task(1)
    def test_header(self):
        header = {"my-sample-header": "Chengdu"}
        r = self.client.get("/", headers=header)
        assert r.status_code == 200


class UserBehaviourPost(TaskSet):

    @task()
    def test_raw_text(self):
        r = self.client.post("/post", headers={'Content-Type': 'text/plain'}, data="I am plain text")
        assert r.status_code == 200


class WebsiteUserGet(HttpLocust):
    # 指向一个TaskSet类，TaskSet类定义了用户的任务信息，该属性为必填；
    task_set = UserBehaviourGet
    # 每个用户执行两个任务间隔时间的上下限（毫秒），具体数值在上下限中随机取值
    wait_time = between(1, 3)
    # 被测系统的host，当在终端中启动locust时没有指定--host参数时才会用到
    host = "https://postman-echo.com"
    # 同时运行多个Locust类时会用到，用于控制不同类型任务的执行权重
    weight = 1


class WebsiteUserPost(HttpLocust):
    task_set = UserBehaviourPost
    wait_time = between(1, 3)
    host = "https://postman-echo.com"
    weight = 2
