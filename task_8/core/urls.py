
from django.urls import path, include
# from .views import BookViewSet, CreateBookView, UpdateBookView, BuyBookView, ListAuthorView, CreateAuthorView, UpdateAuthorView
from .views import BookViewSet, AuthorViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('books', BookViewSet)
router.register('author', AuthorViewSet)

urlpatterns = router.urls
