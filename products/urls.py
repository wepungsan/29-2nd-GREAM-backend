from django.urls import path

from products.views import ProductDetailView, ProductFollowView, ProductSizePriceView, ProductOrderListView, \
    ProductQuoteView, SearchResultView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/follow', ProductFollowView.as_view()),
    path('/size-price/<int:product_id>', ProductSizePriceView.as_view()),
    path('/<int:product_id>/order', ProductOrderListView.as_view()),
    path('/<int:product_id>/quote', ProductQuoteView.as_view()),
    path('/search', SearchResultView.as_view()),
]