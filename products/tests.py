import json

from django.test import TestCase, Client

from biddings.models import BidType, Bidding
from orders.models import Status, Order
from products.models import Product, Category, Theme, Author, Size, Wishlist, ProductSize, ProductImage
from users.models import User


class ProductDetailViewTest(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(
            id   = "1",
            name = "category_1",
        )
        theme_1 = Theme.objects.create(
            id   = "1",
            name = "theme_1",
        )
        author_1 = Author.objects.create(
            id   = "1",
            name = "author_1",
        )
        size_1 = Size.objects.create(
            id   = "1",
            name = "small",
        )
        size_2 = Size.objects.create(
            id   = "2",
            name = "medium",
        )
        size_3 = Size.objects.create(
            id   = "3",
            name = "large",
        )
        bid_type_1 = BidType.objects.create(
            id   = "1",
            name = "bid_type_1",
        )
        user_1 = User.objects.create(
            id       = "1",
            kakao    = "user_1",
            nickname = "user_1",
            email    = "user_1@gmail.com",
        )
        user_2 = User.objects.create(
            id       = "2",
            kakao    = "user_2",
            nickname = "user_2",
            email    = "user_2@gmail.com",
        )
        product_1 = Product.objects.create(
            id            = "1",
            name          = "product_1",
            category      = category_1,
            theme         = theme_1,
            author        = author_1,
            model_number  = "1000",
            release_price = "5000",
            release_date  = "1991-9-26",
        )
        product_size_joined_1 = ProductSize.objects.create(
            id      = "1",
            size    = size_1,
            product = product_1,
        )
        product_size_joined_2 = ProductSize.objects.create(
            id      = "2",
            size    = size_2,
            product = product_1,
        )
        product_size_joined_3 = ProductSize.objects.create(
            id      = "3",
            size    = size_3,
            product = product_1,
        )
        product_image_1 = ProductImage.objects.create(
            id         = "1",
            product    = product_1,
            image_urls = "https://recordsoflife.tistory.com/710",
        )
        bidding_1 = Bidding.objects.create(
            id             = "1",
            product        = product_1,
            size           = size_1,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        bidding_2 = Bidding.objects.create(
            id             = "2",
            product        = product_1,
            size           = size_2,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        bidding_3 = Bidding.objects.create(
            id             = "3",
            product        = product_1,
            size           = size_3,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        status_1 = Status.objects.create(
            id   = "1",
            name = "status_1",
        )
        order_1 = Order.objects.create(
            id       = "1",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_1,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )
        order_2 = Order.objects.create(
            id       = "2",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_2,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )
        order_3 = Order.objects.create(
            id       = "3",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_3,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )

    def test_success_product_detail_view_get_method(self):
        client   = Client()
        response = client.get('/products/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'author'          : 'author_1',
            'buyer_price'     : '5500.55',
            'category'        : 'category_1',
            'category_product': [{
                'product_name'  : 'product_1',
                'product_price' : '5500.55',
                'product_url'   : 'https://recordsoflife.tistory.com/710'
            }],
            'images'          : [{
                'id'            : 1,
                'url'           : 'https://recordsoflife.tistory.com/710'
            }],
            'model_number'    : 1000,
            'name'            : 'product_1',
            'product_id'      : 1,
            'recent_price'    : '5500.55',
            'release_date'    : '1991-09-26T00:00:00',
            'release_price'   : '5000.00',
            'seller_price'    : '5500.55',
            'theme'           : 'theme_1',
            'wishlist'        : []
        })

class ProductFollowViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            name = "test_category"
        )
        theme = Theme.objects.create(
            name = "test_theme"
        )
        author = Author.objects.create(
            name = "test_author"
        )
        product = Product.objects.create(
            id            = "1",
            name          = "test",
            category      = category,
            theme         = theme,
            author        = author,
            release_price = "5000",
            model_number  = "100",
            release_date  = "1991-9-26",
        )
        user = User.objects.create(
            id       = "1",
            kakao    = "test_kakao",
            nickname = "test_nickname",
            email    = "test@gmail.com",
        )
        size = Size.objects.create(
            id   = "1",
            name = "test_size"
        )
        Wishlist.objects.create(
            product = product,
            user    = user,
            size    = size,
        )

    def test_success_product_follow_view_get_method(self):
        client = Client()
        data   = {
            'user_id'    : "1",
            'product_id' : "1",
            'size_id'    : "1",
        }
        response = client.post('/products/follow', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message" : "delete",
        })

class ProductSizePriceTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            name = "test_category"
        )
        theme = Theme.objects.create(
            name = "test_theme"
        )
        author = Author.objects.create(
            name = "test_author"
        )
        product = Product.objects.create(
            id            = "1",
            name          = "test",
            category      = category,
            theme         = theme,
            author        = author,
            release_price = "5000",
            model_number  = "100",
            release_date  = "1991-9-26",
        )
        user = User.objects.create(
            id       = "1",
            kakao    = "test_kakao",
            nickname = "test_nickname",
            email    = "test@gmail.com",
        )
        size = Size.objects.create(
            id   = "1",
            name = "test_size"
        )
        size_2 = Size.objects.create(
            id   = "2",
            name = "test_size"
        )
        size_3 = Size.objects.create(
            id   = "3",
            name = "test_size"
        )
        Wishlist.objects.create(
            product = product,
            user    = user,
            size    = size,
        )
        bid_type = BidType.objects.create(
            id   = "1",
            name = 'test_bid_type_1'
        )
        bid_type_2 = BidType.objects.create(
            id   = "2",
            name = 'test_bid_type_2'
        )
        bidding = Bidding.objects.create(
            id             = "1",
            product        = product,
            size           = size,
            user           = user,
            bid_type       = bid_type,
            purchase_price = 5000.00,
            count          = 10,
            created_at     = "1991-9-26"
        )
        bidding_2 = Bidding.objects.create(
            id             = "2",
            product        = product,
            size           = size_2,
            user           = user,
            bid_type       = bid_type,
            purchase_price = 5000.00,
            count          = 10,
            created_at     = "1991-9-26"
        )
        bidding_3 = Bidding.objects.create(
            id             = "3",
            product        = product,
            size           = size_3,
            user           = user,
            bid_type       = bid_type,
            purchase_price = 5000.00,
            count          = 10,
            created_at     = "1991-9-26"
        )
        bidding_4 = Bidding.objects.create(
            id             = "4",
            product        = product,
            size           = size,
            user           = user,
            bid_type       = bid_type_2,
            purchase_price = 5000.00,
            count          = 10,
            created_at     = "1991-9-26"
        )
        bidding_5 = Bidding.objects.create(
            id             = "5",
            product        = product,
            size           = size_2,
            user           = user,
            bid_type       = bid_type_2,
            purchase_price = 5000.00,
            count          = 10,
            created_at     = "1991-9-26"
        )
        bidding_6 = Bidding.objects.create(
            id             = "6",
            product        = product,
            size           = size_3,
            user           = user,
            bid_type       = bid_type_2,
            purchase_price = 5000.00,
            count          = 10,
            created_at     = "1991-9-26"
        )
        status = Status.objects.create(
            name = "test_status"
        )
        Order.objects.create(
            id       = "1",
            order_no = "550e8400-e29b-41d4-a716-446655440000",
            bidding  = bidding,
            status   = status,
            seller   = user,
            buyer    = user,
        )
        Order.objects.create(
            id       = "2",
            order_no = "550e8400-e29b-41d4-a716-446655440000",
            bidding  = bidding_2,
            status   = status,
            seller   = user,
            buyer    = user,
        )
        Order.objects.create(
            id       = "3",
            order_no = "550e8400-e29b-41d4-a716-446655440000",
            bidding  = bidding_3,
            status   = status,
            seller   = user,
            buyer    = user,
        )
        Order.objects.create(
            id       = "4",
            order_no = "550e8400-e29b-41d4-a716-446655440000",
            bidding  = bidding_4,
            status   = status,
            seller   = user,
            buyer    = user,
        )
        Order.objects.create(
            id       = "5",
            order_no = "550e8400-e29b-41d4-a716-446655440000",
            bidding  = bidding_5,
            status   = status,
            seller   = user,
            buyer    = user,
        )
        Order.objects.create(
            id       = "6",
            order_no = "550e8400-e29b-41d4-a716-446655440000",
            bidding  = bidding_6,
            status   = status,
            seller   = user,
            buyer    = user,
        )

    def test_success_product_size_price_view_get_method(self):
        client   = Client()
        response = client.get('/products/size-price/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "seller_size_price" : [
                {'id' : 1, 'size' : 'test_size', 'date': '1991-09-26', 'price' : '5000.00'},
                {'id' : 2, 'size' : 'test_size', 'date': '1991-09-26', 'price' : '5000.00'},
                {'id' : 3, 'size' : 'test_size', 'date': '1991-09-26', 'price' : '5000.00'},
            ],
            "buyer_size_price"  : [
                {'id' : 4, 'size' : 'test_size', 'date': '1991-09-26', 'price' : '5000.00'},
                {'id' : 5, 'size' : 'test_size', 'date': '1991-09-26', 'price' : '5000.00'},
                {'id' : 6, 'size' : 'test_size', 'date': '1991-09-26', 'price' : '5000.00'},
            ],
        })

class ProductQuoteViewTest(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(
            id   = "1",
            name = "category_1",
        )
        theme_1 = Theme.objects.create(
            id   = "1",
            name = "theme_1",
        )
        author_1 = Author.objects.create(
            id   = "1",
            name = "author_1",
        )
        size_1 = Size.objects.create(
            id   = "1",
            name = "small",
        )
        size_2 = Size.objects.create(
            id   = "2",
            name = "medium",
        )
        size_3 = Size.objects.create(
            id   = "3",
            name = "large",
        )
        bid_type_1 = BidType.objects.create(
            id   = "1",
            name = "bid_type_1",
        )
        user_1 = User.objects.create(
            id       = "1",
            kakao    = "user_1",
            nickname = "user_1",
            email    = "user_1@gmail.com",
        )
        user_2 = User.objects.create(
            id       = "2",
            kakao    = "user_2",
            nickname = "user_2",
            email    = "user_2@gmail.com",
        )
        product_1 = Product.objects.create(
            id            = "1",
            name          = "product_1",
            category      = category_1,
            theme         = theme_1,
            author        = author_1,
            model_number  = "1000",
            release_price = "5000",
            release_date  = "1991-9-26",
        )
        product_size_joined_1 = ProductSize.objects.create(
            id      = "1",
            size    = size_1,
            product = product_1,
        )
        product_size_joined_2 = ProductSize.objects.create(
            id      = "2",
            size    = size_2,
            product = product_1,
        )
        product_size_joined_3 = ProductSize.objects.create(
            id      = "3",
            size    = size_3,
            product = product_1,
        )
        product_image_1 = ProductImage.objects.create(
            id         = "1",
            product    = product_1,
            image_urls = "https://recordsoflife.tistory.com/710",
        )
        bidding_1 = Bidding.objects.create(
            id             = "1",
            product        = product_1,
            size           = size_1,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        bidding_2 = Bidding.objects.create(
            id             = "2",
            product        = product_1,
            size           = size_2,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        bidding_3 = Bidding.objects.create(
            id             = "3",
            product        = product_1,
            size           = size_3,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        status_1 = Status.objects.create(
            id   = "1",
            name = "status_1",
        )
        order_1 = Order.objects.create(
            id       = "1",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_1,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )
        order_2 = Order.objects.create(
            id       = "2",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_2,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )
        order_3 = Order.objects.create(
            id       = "3",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_3,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )

    def test_success_get_product_quote_get_method(self):
        client   = Client()
        response = client.get('/products/1/quote')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'quote': {
                '2022-2-23' : {'quote' : None},
                '2022-2-24' : {'quote' : None},
                '2022-2-25' : {'quote' : None},
                '2022-2-26' : {'quote' : None},
                '2022-2-27' : {'quote' : None},
                '2022-2-28' : {'quote' : None},
                '2022-3-1'  : {'quote' : None},
                '2022-3-2'  : {'quote' : None},
                '2022-3-3'  : {'quote' : None},
                '2022-3-4'  : {'quote' : None},
                '2022-3-5'  : {'quote' : None},
                '2022-3-6'  : {'quote' : None},
                '2022-3-7'  : {'quote' : None},
                '2022-3-8'  : {'quote' : None},
                '2022-3-9'  : {'quote' : None},
                '2022-3-10' : {'quote' : None},
                '2022-3-11' : {'quote' : None},
                '2022-3-12' : {'quote' : None},
                '2022-3-13' : {'quote' : None},
                '2022-3-14' : {'quote' : None},
                '2022-3-15' : {'quote' : None},
                '2022-3-16' : {'quote' : None},
                '2022-3-17' : {'quote' : None},
                '2022-3-18' : {'quote' : None},
                '2022-3-19' : {'quote' : None},
                '2022-3-20' : {'quote' : None},
                '2022-3-21' : {'quote' : None},
                '2022-3-22' : {'quote' : None},
                '2022-3-23' : {'quote' : None},
            }
        })

class SearchResultViewTest(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(
            id   = "1",
            name = "category_1",
        )
        theme_1 = Theme.objects.create(
            id   = "1",
            name = "theme_1",
        )
        author_1 = Author.objects.create(
            id   = "1",
            name = "author_1",
        )
        size_1 = Size.objects.create(
            id   = "1",
            name = "small",
        )
        size_2 = Size.objects.create(
            id   = "2",
            name = "medium",
        )
        size_3 = Size.objects.create(
            id   = "3",
            name = "large",
        )
        bid_type_1 = BidType.objects.create(
            id   = "1",
            name = "bid_type_1",
        )
        user_1 = User.objects.create(
            id       = "1",
            kakao    = "user_1",
            nickname = "user_1",
            email    = "user_1@gmail.com",
        )
        user_2 = User.objects.create(
            id       = "2",
            kakao    = "user_2",
            nickname = "user_2",
            email    = "user_2@gmail.com",
        )
        product_1 = Product.objects.create(
            id            = "1",
            name          = "product_1",
            category      = category_1,
            theme         = theme_1,
            author        = author_1,
            model_number  = "1000",
            release_price = "5000",
            release_date  = "1991-9-26",
        )
        product_size_joined_1 = ProductSize.objects.create(
            id      = "1",
            size    = size_1,
            product = product_1,
        )
        product_size_joined_2 = ProductSize.objects.create(
            id      = "2",
            size    = size_2,
            product = product_1,
        )
        product_size_joined_3 = ProductSize.objects.create(
            id      = "3",
            size    = size_3,
            product = product_1,
        )
        product_image_1 = ProductImage.objects.create(
            id         = "1",
            product    = product_1,
            image_urls = "https://recordsoflife.tistory.com/710",
        )
        bidding_1 = Bidding.objects.create(
            id             = "1",
            product        = product_1,
            size           = size_1,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        bidding_2 = Bidding.objects.create(
            id             = "2",
            product        = product_1,
            size           = size_2,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        bidding_3 = Bidding.objects.create(
            id             = "3",
            product        = product_1,
            size           = size_3,
            user           = user_1,
            bid_type       = bid_type_1,
            purchase_price = 5500.55,
            count          = 10,
            created_at     = "1991-1-1",
        )
        status_1 = Status.objects.create(
            id   = "1",
            name = "status_1",
        )
        order_1 = Order.objects.create(
            id       = "1",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_1,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )
        order_2 = Order.objects.create(
            id       = "2",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_2,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )
        order_3 = Order.objects.create(
            id       = "3",
            order_no = "123e4567-e89b-12d3-a456-556642440000",
            bidding  = bidding_3,
            status   = status_1,
            buyer    = user_1,
            seller   = user_2,
        )

    def test_success_get_product_quote_get_method(self):
        client = Client()
        data   = {
            'keyword' : "pro",
        }
        response = client.post('/products/search', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'product_list' : [{
                'id'     : 1,
                'img_url': 'https://recordsoflife.tistory.com/710',
                'name'   : 'product_1' }],
            'product_num'  : 1
        })
        
class ProductViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            kakao    = "test_kakao",
            nickname = "test_nickname",
            email    = "test_email"
        )
        category = Category.objects.create(
            name = "test_picture"
        )
        theme = Theme.objects.create(
            name = "test_choi"
        )
        size = Size.objects.create(
            name = "test_small"
        )
        author = Author.objects.create(
            name = "test_choi"
        )
        product = Product.objects.create(
            name          = "leekangil",
            category_id   = 1,
            theme_id      = 1,
            author_id     = 1,
            release_price = 1000.00,
            model_number  = "77",
            release_date  = "2010-10-10"
        )
        product_image = ProductImage.objects.create(
            product_id = 1,
            image_urls = "abcde.png"
        )
        wishlist = Wishlist.objects.create(
            product_id = 1,
            user_id    = 1,
            size_id    = 1
        )
    def test_get_method_for_products_list(self):
        client   = Client()
        response = client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message'      : 'SUCCESS',
            'product_list' : [{
                'id'             : 1,
                'name'           : "leekangil",
                'price'          : "1000.00",
                'author'         : "test_choi",
                'wishlist_count' : 1,
                'product_image'  : [{
                    'image' : "abcde.png",
                }]
            }]
        })