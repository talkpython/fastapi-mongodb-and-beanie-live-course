import locust


class PyPIUserMix(locust.FastHttpUser):
    host = "http://localhost:8000"
    wait_time = locust.between(5, 30)

    @locust.task(weight=1)
    def home(self):
        self.client.get('/')

    @locust.task(weight=5)
    def search(self):
        self.client.get('/api/packages/search/fastapi')
        self.client.get('/api/packages/details/prometheus-fastapi-instrumentator')

    # @locust.task()
    # def package_details(self):
    #     self.client.get('/api/packages/details/fastapi')
