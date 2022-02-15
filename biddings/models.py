from django.db import models

class Bidding(models.Model):
    product_id     = models.ForeignKey('Product', on_delete = models.CASCADE, related_name = 'bidding')
    user_id        = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'bidding')
    bid_type_id    = models.ForeignKey('Bid_type', on_delete = models.CASCADE, related_name = 'bidding')
    purchase_price = models.DecimalField(max_digits = 15, decimal_places = 2)
    count          = models.IntegerField()

    class Meta:
        db_table = 'biddings'

class Bid_Type(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'bid_types'