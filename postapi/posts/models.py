from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    keywords = models.TextField(max_length=500)
    url = models.URLField(max_length=1024)
    author_ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PostHistory(models.Model):
    OPERATION_CHOICES = (
        ('update', 'Update'),
        ('delete', 'Delete'),
    )
    post = models.ForeignKey(Post, related_name="histories", on_delete=models.SET_NULL, null=True)
    original_post_id = models.IntegerField(null=True, blank=True)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    data = models.JSONField()
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by_ip = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.operation} on {self.post} at {self.modified_at}"