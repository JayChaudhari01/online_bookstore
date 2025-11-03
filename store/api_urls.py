# store/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# अगर बाद में viewsets बनाओ तो register करो, उदाहरण:
# from .api_views import BookViewSet
# router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
