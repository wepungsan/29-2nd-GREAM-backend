from django.db import models

class User(models.Model):
    kakao_id   = models.CharField(max_length = 50)
    nickname   = models.CharField(max_length = 50)
    email      = models.EmailField()
    deleted_at = models.DateTimeField(null = True)

    class Meta:
        db_table = 'users'