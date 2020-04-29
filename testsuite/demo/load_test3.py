from locust import HttpLocust, TaskSet, task, between


class Stay(TaskSet):

    # @staticmethod
    # def on_start(self):
    #     """ 定义每个 Locust 用户开始做的第一件事 on_start is called when a Locust start before any task is scheduled """
    #     print(self)
    #     print("start test")

    # 通过@task()装饰的方法为一个事务。方法的参数用于指定该行为的执行权重。参数越大每次被虚拟用户执行的概率越高。如果不设置默认为1
    @task(3)
    def read_book(self):
        print('I am reading a book.')

    @task(7)
    def listen_music(self):
        print('I am listening to music.')

    @task(1)
    def log_out(self):
        # 顶层的TaskSet（即被绑定到某个Locust类的task_set的第一层TaskSet）不能调用这个方法。reschedule置为True时，从被嵌套任务出来马上选择新任务执行，如果置为False，从被嵌套任务出来后，随机等待min_wait和max_wait之间的一段时间，再选择新任务执行。
        self.interrupt()


class UserTask(TaskSet):
    # 表示每个用户执行 stay 的频率是2，也就的 UserTask 的两倍。
    tasks = {Stay: 2}

    @task(1)
    def leave(self):
        print('I don not like this page.')


class User(HttpLocust):
    task_set = UserTask
    wait_time = between(5, 15)
    host = "https://www.baidu.com"

