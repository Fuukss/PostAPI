from django.test import RequestFactory
from rest_framework.test import APITestCase
from posts.models import Post, PostHistory
from posts.serializers import PostSerializer


class PostSerializerTest(APITestCase):
    """
    Tests for the PostSerializer to verify validation and representation.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.META['REMOTE_ADDR'] = '127.0.0.1'

        self.valid_data = {
            "name": "Test Post",
            "description": "Example post description.",
            "keywords": ["word1", "word2", "word3"],
            "url": "http://example.com"
        }
        self.invalid_data_less_keywords = {
            "name": "Test Post",
            "description": "Example description.",
            "keywords": ["word1", "word2"],
            "url": "http://example.com"
        }
        self.invalid_data_name_in_keywords = {
            "name": "Test Post",
            "description": "Example description.",
            "keywords": ["Test Post", "word2", "word3"],
            "url": "http://example.com"
        }
        long_keyword = "a" * 498
        self.invalid_data_long_keywords = {
            "name": "Test Post",
            "description": "Example description.",
            "keywords": [long_keyword, "word2", "word3"],
            "url": "http://example.com"
        }

    def test_serializer_valid(self):
        # Arrange & Act: Create a serializer instance with valid data and proper request context
        serializer = PostSerializer(data=self.valid_data, context={"request": self.request})
        is_valid = serializer.is_valid()
        # Assert
        self.assertTrue(is_valid, serializer.errors)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["keywords"], self.valid_data["keywords"])
        # Simulate instance creation so that the create() method is used
        post = serializer.create(validated_data)
        rep = serializer.to_representation(post)
        self.assertEqual(rep["keywords"], self.valid_data["keywords"])

    def test_serializer_invalid_less_keywords(self):
        # Arrange & Act
        serializer = PostSerializer(data=self.invalid_data_less_keywords, context={"request": self.request})
        is_valid = serializer.is_valid()
        # Assert
        self.assertFalse(is_valid)
        self.assertIn("At least 3 unique keywords are required", str(serializer.errors))

    def test_serializer_invalid_name_in_keywords(self):
        # Arrange & Act
        serializer = PostSerializer(data=self.invalid_data_name_in_keywords, context={"request": self.request})
        is_valid = serializer.is_valid()
        # Assert
        self.assertFalse(is_valid)
        self.assertIn("The name must not be one of the keywords", str(serializer.errors))

    def test_serializer_invalid_long_keywords(self):
        # Arrange & Act
        serializer = PostSerializer(data=self.invalid_data_long_keywords, context={"request": self.request})
        is_valid = serializer.is_valid()
        # Assert
        self.assertFalse(is_valid)
        self.assertIn("The combined length of keywords exceeds 500 characters", str(serializer.errors))
