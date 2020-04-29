from locust import HttpLocust, TaskSet, task, between


class UserBehaviourGet(TaskSet):

    @task(2)
    def test_para(self):
        parameters = {"City": "Chengdu", "Location": "SoftwarePark"}
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
    task_set = UserBehaviourGet
    wait_time = between(1, 3)
    host = "https://postman-echo.com"


class WebsiteUserPost(HttpLocust):
    task_set = UserBehaviourPost
    wait_time = between(1, 3)
    host = "https://postman-echo.com"
