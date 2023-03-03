from django.db import models

# Create your models here.


def upload_to(instance, filename):
    return 'pitch/{filename}'.format(filename=filename)


class Company(models.Model):

    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    pitch_uploaded = models.FileField(upload_to=upload_to,
                                      blank=True,
                                      null=True)

    emailTo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
