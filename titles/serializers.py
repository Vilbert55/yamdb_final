from rest_framework import serializers

from .models import Title, Category, Genre, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateUpdateSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:        
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment
