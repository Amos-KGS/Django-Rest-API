from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    genre = models.CharField(max_length=200)
    price = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)