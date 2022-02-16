from django.db import models

class Order(models.Model):
    order_no   = models.UUIDField()
    bidding    = models.ForeignKey('biddings.Bidding', models.CASCADE, related_name = 'order')
    status     = models.ForeignKey('Status', models.DO_NOTHING, related_name = 'order')
    buyer      = models.ForeignKey('users.User', models.DO_NOTHING, related_name = 'buyer')
    seller     = models.ForeignKey('users.User', models.DO_NOTHING, related_name = 'seller')
    created_at = models.DateField()    

    class Meta:
        db_table = 'orders'

class Status(models.Model):
    name = models.CharField(max_length = 50, null = False)

    class Meta:
        db_table = 'statuses'
