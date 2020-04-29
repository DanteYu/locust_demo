from locust import HttpLocust, TaskSequence, task, between, seq_task


class UserBehaviourGet(TaskSequence):

    @seq_task(1)
    @task()
    def test_para(self):
        parameters = {"City": "Chengdu", "Location": "SoftwarePark"}
        r = self.client.get("/get", params=parameters)
        assert r.status_code == 200

    @seq_task(2)
    @task()
    def test_header(self):
        header = {"my-sample-header": "Chengdu"}
        r = self.client.get("/", headers=header)
        assert r.status_code == 200

    @seq_task(3)
    @task()
    def test_now(self):
        r = self.client.get("/time/now")
        assert r.status_code == 200


class WebsiteUserGet(HttpLocust):
    task_set = UserBehaviourGet
    wait_time = between(1, 3)
    host = "https://postman-echo.com"

