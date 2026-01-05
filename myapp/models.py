from django.db import models
from django.urls import reverse

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100, blank=True)
    email      = models.EmailField(unique=True)
    age        = models.PositiveIntegerField()
    photo      = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    def get_absolute_url(self):
        return reverse('student:detail', kwargs={'pk': self.pk})
    
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # REQUIRED FOR DRF AUTH
    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username