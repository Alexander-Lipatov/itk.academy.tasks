from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer, BuyBookSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'author__first_name', 'author__last_name')


    @method_decorator(cache_page(60 * 15))
    def list(self, request):
        return super().list(request)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(url_path='buy', detail=True, methods=['post'])
    def buy_book(self, request, pk=None):
        count = request.data.get('count', 0)
        book: Book = self.get_object()

        buy_serializer = BuyBookSerializer(data=request.data)
        if buy_serializer.is_valid():
            book.buy_book(count)
            return Response(self.serializer_class(book).data, status=200)
        return Response(buy_serializer.data, status=400)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request):
        return super().list(request)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, pk=None):
        return super().list(request)
