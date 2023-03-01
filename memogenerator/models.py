from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    pitch_uploaded = models.FileField(
        upload_to='mediafiles/', null=True, blank=True)
    emailTo = models.CharField(max_length=100, null=True, blank=True
                               )
    def __str__(self):
        return self.name
