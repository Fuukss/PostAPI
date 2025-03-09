from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post, PostHistory

class PostAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Arrange: Define test data in English for all tests
        cls.valid_data = {
            "name": "Test Post",
            "description": "Example post description.",
            "keywords": ["word1", "word2", "word3"],
            "url": "http://example.com"
        }
        cls.invalid_data_less_keywords = {
            "name": "Test Post",
            "description": "Example description.",
            "keywords": ["word1", "word2"],
            "url": "http://example.com"
        }
        cls.invalid_data_name_in_keywords = {
            "name": "Test Post",
            "description": "Example description.",
            "keywords": ["Test Post", "word2", "word3"],
            "url": "http://example.com"
        }
        long_keyword = "a" * 498
        cls.invalid_data_long_keywords = {
            "name": "Test Post",
            "description": "Example description.",
            "keywords": [long_keyword, "word2", "word3"],
            "url": "http://example.com"
        }

    def test_create_valid_post(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        # Act
        response = self.client.post(list_url, self.valid_data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data.get('author_ip'), '127.0.0.1')
        self.assertEqual(data.get('keywords'), self.valid_data['keywords'])

    def test_create_invalid_less_keywords(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        # Act
        response = self.client.post(list_url, self.invalid_data_less_keywords, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_name_in_keywords(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        # Act
        response = self.client.post(list_url, self.invalid_data_name_in_keywords, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_long_keywords(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        # Act
        response = self.client.post(list_url, self.invalid_data_long_keywords, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_endpoint_returns_keywords_as_list(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        create_response = self.client.post(list_url, self.valid_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # Act
        list_response = self.client.get(list_url, format='json')
        # Assert
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        for entry in list_response.json():
            self.assertIsInstance(entry.get('keywords'), list)

    def test_update_post_same_ip(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        create_response = self.client.post(list_url, self.valid_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_id = create_response.json().get('id')
        detail_url = reverse('post-detail', args=[post_id])
        update_data = {
            "name": "Updated Post",
            "description": "Updated description.",
            "keywords": ["word1", "word2", "word4"],
            "url": "http://example.com/updated"
        }
        # Act
        update_response = self.client.put(detail_url, update_data, format='json')
        # Assert
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        post = Post.objects.get(id=post_id)
        self.assertEqual(post.histories.count(), 1)
        history = post.histories.first()
        self.assertEqual(history.operation, 'update')
        self.assertEqual(history.modified_by_ip, '127.0.0.1')

    def test_update_post_different_ip(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        create_response = self.client.post(list_url, self.valid_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_id = create_response.json().get('id')
        detail_url = reverse('post-detail', args=[post_id])
        self.client.defaults['REMOTE_ADDR'] = '192.168.1.1'
        update_data = {
            "name": "Updated Post",
            "description": "Updated description.",
            "keywords": ["word1", "word2", "word4"],
            "url": "http://example.com/updated"
        }
        # Act
        update_response = self.client.put(detail_url, update_data, format='json')
        # Assert
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_same_ip(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        create_response = self.client.post(list_url, self.valid_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_id = create_response.json().get('id')
        detail_url = reverse('post-detail', args=[post_id])
        # Act
        delete_response = self.client.delete(detail_url, format='json')
        # Assert
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        histories = PostHistory.objects.filter(original_post_id=post_id)
        self.assertEqual(histories.count(), 1)
        self.assertEqual(histories.first().operation, 'delete')

    def test_delete_post_different_ip(self):
        # Arrange
        list_url = reverse('post-list')
        self.client.defaults['REMOTE_ADDR'] = '127.0.0.1'
        create_response = self.client.post(list_url, self.valid_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_id = create_response.json().get('id')
        detail_url = reverse('post-detail', args=[post_id])
        self.client.defaults['REMOTE_ADDR'] = '192.168.1.1'
        # Act
        delete_response = self.client.delete(detail_url, format='json')
        # Assert
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
