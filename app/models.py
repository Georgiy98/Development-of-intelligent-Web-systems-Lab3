from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    name = models.CharField(null=False, max_length=128, blank=False)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_ids', null=True, blank=True)

# Create your models here.
