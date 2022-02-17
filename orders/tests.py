from django.test import TestCase, Client

from biddings.models import Bidding, BidType
from orders.models import Order, Status
from products.models import Product, Category, Theme, Author, Size, Wishlist
from users.models import User


class ProductOrderListTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            name="test_category"
        )
        theme = Theme.objects.create(
            name="test_theme"
        )
        author = Author.objects.create(
            name="test_author"
        )
        product = Product.objects.create(
            name="test",
            category=category,
            theme=theme,
            author=author,
            release_price="5000",
            model_number="100",
            release_date="1991-9-26",
        )
        user = User.objects.create(
            kakao="test_kakao",
            nickname="test_nickname",
            email="test@gmail.com",
        )
        size = Size.objects.create(
            name="test_size"
        )
        Wishlist.objects.create(
            product=product,
            user=user,
            size=size,
        )
        bid_type = BidType.objects.create(
            name='test_bid_type'
        )
        bidding = Bidding.objects.create(
            product=product,
            size=size,
            user=user,
            bid_type=bid_type,
            purchase_price=5000.00,
            count=10,
            created_at="1991-9-26"
        )
        status = Status.objects.create(
            name="test_status"
        )
        Order.objects.create(
            order_no="550e8400-e29b-41d4-a716-446655440000",
            bidding=bidding,
            status=status,
            seller=user,
            buyer=user,
        )

    def test_success_order_list_view_get_method(self):
        client = Client()
        response = client.get('/orders/list/1?size=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'orders': [{
                'bid_type': 'test_bid_type',
                'count': 10,
                'created_at': '1991-09-26',
                'name': 'test',
                'price': '5000.00',
                'size': 'test_size'
            }]
        })



