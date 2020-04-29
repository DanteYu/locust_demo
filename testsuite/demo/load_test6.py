from locust import HttpLocust, TaskSet, task, between

class ForumPage(TaskSet):
    @task(20)
    def read_thread(self):
        pass

    @task(1)
    def new_thread(self):
        pass

    #能够退出forumpage的执行，避免一直执行
    @task(5)
    def stop(self):
        self.interrupt()

# 内嵌的taskset   使用tasks属性
class UserBehaviour(TaskSet):
    tasks = {ForumPage:10}

    @task
    def index(self):
        pass

#
# class MyTaskSet(TaskSet):
#     @task
#     class SubTaskSet(TaskSet):
#         @task
#         def my_task(self):
#             pass