from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Содержание статьи')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото', blank=False)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey('CategoryArticle', on_delete=models.PROTECT,
                                 verbose_name='Категория статьи', )

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=100))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_article', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-pub_date']


class CategoryArticle(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория статьи'
        verbose_name_plural = 'Категории статей'
        ordering = ['title']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField(max_length=50, verbose_name='Имя автора')
    content = models.CharField(max_length=300, verbose_name='Текст комментария')
    email = models.EmailField(max_length=254, verbose_name='Email')
    created_ad = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['-created_ad']
