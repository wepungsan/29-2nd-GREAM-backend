import json
from datetime import datetime, timedelta
from enum import Enum

from dateutil.relativedelta import relativedelta
from django.db.models import Q, Max, Min, Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from core.decorator import login_decorator
from orders.models import Order
from products.models import Product, Wishlist, Size, Category
from users.models import User

class ProductSizeType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class BidType(Enum):
    SELLER = 1
    BUYER = 2

class ProductDetailView(View):
    def filter_order(self, product_id, size:ProductSizeType=None):
        if size:
            size = size.value
            return Order.objects.filter(bidding__product=product_id, bidding__size=size) \
                .order_by("-bidding__created_at").first().bidding.purchase_price
        else:
            return Order.objects.filter(bidding__product=product_id)\
                .order_by("-bidding__created_at").first().bidding.purchase_price

    def get_price_by_product(self, product_id):
        recent_price = self.filter_order(product_id)
        small_recent_price = self.filter_order(product_id, ProductSizeType.SMALL)
        medium_recent_price = self.filter_order(product_id, ProductSizeType.MEDIUM)
        large_recent_price = self.filter_order(product_id, ProductSizeType.LARGE)
        size_price_list = [small_recent_price, medium_recent_price, large_recent_price]
        seller_price = max(size_price_list)
        buyer_price = min(size_price_list)
        return [recent_price, seller_price, buyer_price]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        price_list = self.get_price_by_product(product_id)

        images = product.productimage_set.all()
        image_list = [{
            "id": image.id,
            "url": image.image_urls,
        } for image in images]

        wishlists = Wishlist.objects.filter(product=product_id)
        wishlist_list = [{
            "product_id" : wishlist.product.id,
            "size" : wishlist.size.name,
        } for wishlist in wishlists]

        category_products = Product.objects.filter(category=product.category.id)[:5]
        category_product_list = [{
            "product_id" : product.id,
            "product_name" : product.name,
            "product_url" : product.productimage_set.first().image_urls,
            "product_price" : min([
                product.bidding.filter(size=1).first().purchase_price,
                product.bidding.filter(size=2).first().purchase_price,
                product.bidding.filter(size=3).first().purchase_price,
            ])
        } for product in category_products]

        return JsonResponse({
            "product_id": product.id,
            "name": product.name,
            "category": product.category.name,
            "theme": product.theme.name,
            "author": product.author.name,
            "release_price": product.release_price,
            "model_number": product.model_number,
            "release_date": product.release_date,
            "wishlist": wishlist_list,
            "images": image_list,
            "recent_price": price_list[0],
            "seller_price": price_list[1],
            "buyer_price": price_list[2],
            "category_product": category_product_list,
        }, status=200)

class ProductFollowView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = request.user
            user_id = user.id
            product_id = int(data['product_id'])
            size_id = int(data['size_id'])

            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            size = Size.objects.get(id=size_id)

            wishlist, created = Wishlist.objects.get_or_create(
                user=user,
                product=product,
                size=size,
            )

            if not created:
                wishlist.delete()
                return JsonResponse({
                    "message": "delete",
                }, status=200)
            else:
                return JsonResponse({
                    "message": "create",
                }, status=200)
        except KeyError:
            return JsonResponse({"message": "Key Error"}, status=403)
        except User.DoesNotExist:
            return JsonResponse({"message": "User DoesNotExist"}, status=403)
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product DoesNotExist"}, status=403)
        except Size.DoesNotExist:
            return JsonResponse({"message": "Size DoesNotExist"}, status=403)

class ProductSizePriceView(View):
    def filter_order(self, product_id, size:ProductSizeType, bid_type:BidType):
        size = size.value
        bid_type = bid_type.value
        orders = Order.objects.filter(bidding__product=product_id, bidding__size=size, bidding__bid_type=bid_type)
        return orders.filter(bidding__size=size, bidding__bid_type=bid_type).order_by("-bidding__created_at").first()

    def get_recent_order_by_product(self, product_id):
        seller_recent_small_order = self.filter_order(product_id, ProductSizeType.SMALL, BidType.SELLER)
        seller_recent_medium_order = self.filter_order(product_id, ProductSizeType.MEDIUM, BidType.SELLER)
        seller_recent_large_order = self.filter_order(product_id, ProductSizeType.LARGE, BidType.SELLER)
        buyer_recent_small_order = self.filter_order(product_id, ProductSizeType.SMALL, BidType.BUYER)
        buyer_recent_medium_order = self.filter_order(product_id, ProductSizeType.MEDIUM, BidType.BUYER)
        buyer_recent_large_order = self.filter_order(product_id, ProductSizeType.LARGE, BidType.BUYER)
        return {
            "seller_small" : seller_recent_small_order,
            "seller_medium" : seller_recent_medium_order,
            "seller_large" : seller_recent_large_order,
            "buyer_small" : buyer_recent_small_order,
            "buyer_medium" : buyer_recent_medium_order,
            "buyer_large" : buyer_recent_large_order,
        }

    def get(self, request, product_id):
        recent_order = self.get_recent_order_by_product(product_id)

        seller_price = [
            {
                "id": recent_order["seller_small"].id,
                "size": recent_order["seller_small"].bidding.size.name,
                "date": recent_order["seller_small"].bidding.created_at,
                "price": recent_order["seller_small"].bidding.purchase_price,
            },
            {
                "id": recent_order["seller_medium"].id,
                "size": recent_order["seller_medium"].bidding.size.name,
                "date": recent_order["seller_medium"].bidding.created_at,
                "price": recent_order["seller_medium"].bidding.purchase_price,
            },
            {
                "id": recent_order["seller_large"].id,
                "size": recent_order["seller_large"].bidding.size.name,
                "date": recent_order["seller_large"].bidding.created_at,
                "price": recent_order["seller_large"].bidding.purchase_price,
            },
        ]

        buyer_price = [
            {
                "id": recent_order["buyer_small"].id,
                "size": recent_order["buyer_small"].bidding.size.name,
                "date": recent_order["buyer_small"].bidding.created_at,
                "price": recent_order["buyer_small"].bidding.purchase_price,
            },
            {
                "id": recent_order["buyer_medium"].id,
                "size": recent_order["buyer_medium"].bidding.size.name,
                "date": recent_order["buyer_medium"].bidding.created_at,
                "price": recent_order["buyer_medium"].bidding.purchase_price,
            },
            {
                "id": recent_order["buyer_large"].id,
                "size": recent_order["buyer_large"].bidding.size.name,
                "date": recent_order["buyer_large"].bidding.created_at,
                "price": recent_order["buyer_large"].bidding.purchase_price,
            },
        ]

        return JsonResponse({
            "seller_size_price": seller_price,
            "buyer_size_price": buyer_price,
        }, status=200)

class ProductOrderListView(View):
    def get(self, request, product_id):
        size_id = request.GET.get('size')

        q = Q(bidding__product=product_id)

        if size_id:
            q &= Q(bidding__size=size_id)

        orders = Order.objects.filter(q).order_by("-bidding__created_at")

        orders = orders.select_related('bidding', 'bidding__product', 'bidding__size', 'bidding__bid_type',)

        order_list = [{
            "name" : order.bidding.product.name,
            "size" : order.bidding.size.name,
            "bid_type" : order.bidding.bid_type.name,
            "price" : order.bidding.purchase_price,
            "count" : order.bidding.count,
            "created_at" : order.bidding.created_at,
        } for order in orders]

        return JsonResponse({
            "orders" : order_list
        }, status=200)

class ProductQuoteView(View):
    def get(self, request, product_id):
        str_start_date = datetime.now().strftime("%Y-%m-%d")

        start_date = datetime.strptime(str_start_date, "%Y-%m-%d")
        last_date = start_date + relativedelta(months=1)

        quote_dict = {}

        copy_start = start_date
        copy_last = last_date

        while start_date <= last_date:
            orders = Order.objects.filter(bidding__product=product_id, bidding__created_at=start_date)
            orders_avg = orders.aggregate(quote = Avg('bidding__purchase_price'))
            if orders_avg['quote'] == None:
                orders_avg = Order.objects.filter(
                    bidding__product=product_id,
                    bidding__created_at__range=[copy_start, copy_last]
                ).aggregate(quote = Avg('bidding__purchase_price'))
            quote_dict[str(start_date.year) + "-" + str(start_date.month) + "-" + str(start_date.day)] = orders_avg
            start_date += timedelta(days=1)

        return JsonResponse({
            "quote": quote_dict,
        }, status=200)

class SearchResultView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            keyword = data['keyword']
            products = Product.objects.filter(name__icontains=keyword)
            filtered_products = products[:5]
            product_list = [
                {
                    "id" : product.id,
                    "name" : product.name,
                    "img_url" : product.productimage_set.first().image_urls
                } for product in filtered_products
            ]
            return JsonResponse({
                "product_list": product_list,
                "product_num" : len(products)
            }, status=200)
        except KeyError:
            return JsonResponse({"message": "Key Error"}, status=403)