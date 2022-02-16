from django.db import models

from core.models import TimeStamp

class User(TimeStamp):
    kakao      = models.CharField(max_length = 50)
    nickname   = models.CharField(max_length = 50)
    email      = models.EmailField()
    deleted_at = models.DateTimeField(null = True)

    class Meta:
        db_table = 'users'