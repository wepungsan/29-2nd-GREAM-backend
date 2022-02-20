from nturl2path import url2pathname
from django.urls import path
from users.views import KakaoLoginView

urlpatterns = [
    path('/login', KakaoLoginView.as_view()),
]