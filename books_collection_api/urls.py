from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import BookListView, OpinionViewSet

router = DefaultRouter()
router.register(r'opinions', OpinionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('books/', BookListView.as_view(), name='book-list'),
]
