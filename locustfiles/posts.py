from random import randint
from locust import task, constant, HttpUser


class GetRequests(HttpUser):
    host = "http://localhost:8000"

    wait_time = constant(0.5)
    weight = 5

    @task(10)
    def get_index(self):
        self.client.get('/')

    @task(6)
    def get_category_posts(self):
        cat_id = randint(1, 7)
        self.client.get(f"/category-posts/{cat_id}")

    @task(6)
    def get_tag_posts(self):
        tag_id = randint(1, 7)
        self.client.get(f"/tag-posts/{tag_id}")

    @task(3)
    def get_post_detail(self):
        tag_id = randint(1, 50)
        self.client.get(f"/post-detail/{tag_id}/")

    @task(1)
    def get_add_post(self):
        self.client.get(f"/add-post/")

    @task(1)
    def get_login(self):
        self.client.get("/accounts/sign-in/")

    @task(1)
    def get_sign_up(self):
        self.client.get("/accounts/sign-up/")

    @task(1)
    def get_edit_profile(self):
        profile_id = randint(1, 7)
        self.client.get(f"/edit-profile/{profile_id}/")


    @task(6)
    def get_test_cache(self):
        self.client.get('/test-cache/')



class PostRequests(HttpUser):
    host = "http://localhost:8000"

    wait_time = constant(0.5)
    weight = 3

    @task(2)
    def post_sign_in(self):
        r = self.client.get('')
        self.client.post('/accounts/sign-in/',
                            {"username":"shania", 
                            "password":"root12345",
                            'csrfmiddlewaretoken': r.cookies['csrftoken']})
    @task(2)  
    def post_sign_up(self):
        r = self.client.get('')
        self.client.post('/accounts/sign-up/',
                            {"username":"shania", 
                            "first_name":'f',
                            "last_name": 'l',
                            "email": "a@b.com",
                            "password1":"root12345",
                            "password2":"root12345",
                            'csrfmiddlewaretoken': r.cookies['csrftoken']})
        
    @task(2)  
    def post_add_post(self):
        r = self.client.get('')
        self.client.post('/accounts/add-post/',
                            {'title': 'a',
                             'body': 'b',
                             'category': [1],
                             'csrfmiddlewaretoken': r.cookies['csrftoken']},
                             {'header_image': ''})
        


