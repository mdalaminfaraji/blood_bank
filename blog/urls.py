from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, BlogImageViewSet, AuthorViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'blog-images', BlogImageViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
