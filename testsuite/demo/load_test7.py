from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        # GET login page to get csrftoken from it
        response = self.client.get('/accounts/login/')
        csrftoken = response.cookies['csrftoken']
        # POST to login page with csrftoken
        self.client.post('/accounts/login/',
                         {'username': 'username', 'password': 'P455w0rd'},
                         headers={'X-CSRFToken': csrftoken})

    @task(1)
    def index(self):
        self.client.get('/')

    @task(2)
    def heavy_url(self):
        self.client.get('/heavy_url/')

    @task(2)
    def another_heavy_ajax_url(self):
        # ajax GET
        self.client.get('/another_heavy_ajax_url/',
        headers={'X-Requested-With': 'XMLHttpRequest'})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior