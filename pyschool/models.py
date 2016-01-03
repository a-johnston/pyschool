from django.conf import settings
from django.db import models

class UserProgress(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    level = models.IntegerField()

    completed = models.TextField()
    
    def __unicode__(self):
        return str(user)

class ChallengeSet(models.Model):
    name = models.CharField(max_length=30)

    values = models.TextField()
    pass
