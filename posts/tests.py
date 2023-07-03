from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTest(APITestCase):
    def setUp(self):
        '''
        Runs before any other test.
        Creates user for referencing in tests.
        '''
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        '''
        Test to list the posts in the database
        1. get adam - newly created user
        2. asociate newly created post with that user (adam)
        3. test to get a get request to posts
        '''
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        '''
        Test that logged in user can create a post
        1. log in using the api test client
        2. make a post request to posts
        3. count objects
        4. check if there is only one
        '''
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_can_not_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
