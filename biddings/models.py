from django.db import models

class Bidding(models.Model):
    product        = models.ForeignKey('products.Product', on_delete = models.CASCADE, related_name = 'bidding')
    size           = models.ForeignKey('products.Size', on_delete = models.CASCADE, related_name = 'bidding')
    user           = models.ForeignKey('users.User', on_delete = models.CASCADE, related_name = 'bidding')
    bid_type       = models.ForeignKey('BidType', on_delete = models.CASCADE, related_name = 'bidding')
    purchase_price = models.DecimalField(max_digits = 15, decimal_places = 2)
    count          = models.IntegerField()
    created_at     = models.DateField()

    class Meta:
        db_table = 'biddings'

class BidType(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'bid_types'