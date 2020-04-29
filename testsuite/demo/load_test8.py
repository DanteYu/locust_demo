from lxml import etree
from locust import TaskSet, task, HttpLocust, between

class UserBehavior(TaskSet):

    # 在某些请求中，需要携带之前从Server端返回的参数，因此在构造请求时需要先从之前的Response中提取出所需的参数
    @staticmethod
    def get_session(html):
        tree = etree.HTML(html)
        return tree.xpath("//div[@class='btnbox']/input[@name='session']/@value")[0]

    @task(10)
    def test_login(self):
        html = self.client.get('/login').text
        username = 'user@compay.com'
        password = '123456'
        session = self.get_session(html)
        payload = {
            'username': username,
            'password': password,
            'session': session
        }
        self.client.post('/login', data=payload)

class WebsiteUser(HttpLocust):
    host = 'https://debugtalk.com'
    task_set = UserBehavior
    wait_time = between(1, 3)