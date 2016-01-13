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
        return str(self.user) + ' ' + str(self.level)
