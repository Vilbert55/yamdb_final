from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

from user_api.models import User


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(verbose_name='URL', max_length=20, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(verbose_name='URL', max_length=20, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year = models.PositiveSmallIntegerField(default=0)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(max_length=400, blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def update_rating(self):
        reviews = Review.objects.select_related('author').filter(title=self)
        score = reviews.aggregate(Avg('score'))['score__avg']
        self.rating = int(round(score))
        self.save()


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=5000)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
