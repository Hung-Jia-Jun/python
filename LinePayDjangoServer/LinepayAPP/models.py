from django.db import models


class clientSession(models.Model):
    name = models.TextField()
    status = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
