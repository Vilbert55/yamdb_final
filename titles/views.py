from rest_framework import filters, viewsets, generics, serializers, mixins

from user_api.permissions import IsOwnerOrAdminOrModeratorOrReadOnly, AdminOrReadOnly
from .filters import TitleFilter
from .models import Title, Category, Genre, Review, Comment
from .serializers import (
    TitleSerializer, TitleCreateUpdateSerializer,
    CategorySerializer, GenreSerializer, 
    ReviewSerializer, CommentSerializer
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()    
    filterset_class = TitleFilter    
    permission_classes = [AdminOrReadOnly,]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return TitleCreateUpdateSerializer
        return TitleSerializer  


class CategoryListCreateDeleteView(
    mixins.ListModelMixin, mixins.DestroyModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
    ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreListCreateDeleteView(
    mixins.ListModelMixin, mixins.DestroyModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
    ):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdminOrModeratorOrReadOnly,]

    def get_queryset(self):
        queryset = self.queryset.filter(title_id=self.kwargs.get('title_id'))
        return queryset

    def perform_create(self, serializer):        
        title_id = self.kwargs.get('title_id')
        title = generics.get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise serializers.ValidationError('Already reviewed')
        serializer.save(author=self.request.user, title=title)        
        title.update_rating()

    def perform_update(self, serializer):        
        title_id = self.kwargs.get('title_id')
        title = generics.get_object_or_404(Title, pk=title_id)               
        serializer.save()        
        title.update_rating()
        
    def perform_destroy(self, instance):
        instance.delete()
        title_id = self.kwargs.get('title_id')
        title = generics.get_object_or_404(Title, pk=title_id)
        title.update_rating()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdminOrModeratorOrReadOnly,]

    def get_queryset(self):
        title = generics.get_object_or_404(Title,  pk=self.kwargs.get('title_id'))
        review = generics.get_object_or_404(Review,  pk=self.kwargs.get('review_id'), title=title)
        return self.queryset.filter(review=review)

    def perform_create(self, serializer):   
        title = generics.get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = generics.get_object_or_404(Review, pk=self.kwargs.get('review_id'), title=title)
        serializer.save(author=self.request.user, review=review)
