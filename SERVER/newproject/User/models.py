from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/')
    fprint = models.BinaryField()
    codebar = models.CharField(max_length=100, unique=True, null=True, blank=True) 

    def __str__(self):
        return f"{self.name} {self.fname}"