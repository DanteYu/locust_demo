from locust import HttpLocust, TaskSet, task, between


class UserTask(TaskSet):

    @task
    def job(self):
        with self.client.get('/', catch_response=True) as response:
            if response.status_code == 200:
                response.failure
                response.failure('Failed!')
            else:
                response.success()


class User(HttpLocust):
    task_set = UserTask
    wait_time = between(1, 4)
    host = "https://www.baidu.com"
