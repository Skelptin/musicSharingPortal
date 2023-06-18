from django.db import models
from django.contrib.auth import get_user_model

class Music(models.Model):
    ACCESS_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(upload_to='music/')
    access = models.CharField(max_length=10, choices=ACCESS_CHOICES)

    allowed_emails = models.TextField(blank=True, null=True, help_text="Comma-separated emails for protected access")

    def __str__(self):
        return self.file.name
