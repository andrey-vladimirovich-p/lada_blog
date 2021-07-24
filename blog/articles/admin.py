from django.contrib import admin
from django import forms
from django.forms import Textarea
from django.utils.safestring import mark_safe
from .models import Article, CategoryArticle, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db import models


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(),)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('id', 'title', 'category', 'get_photo', 'pub_date', 'is_published', 'views')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'pub_date', 'views',
              'is_published')
    readonly_fields = ('pub_date', 'get_photo', )
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return "Фото не установлено"
    get_photo.short_description = 'Миниатюра'


class CategoryArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'content', 'email', 'created_ad', 'is_active')
    list_display_links = ('article', 'author')
    fields = ('article', 'author', 'content', 'email', 'created_ad', 'is_active')
    readonly_fields = ('created_ad', )
    list_editable = ('content', 'is_active')
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 5, 'cols': 40})},
    }


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CategoryArticle, CategoryArticleAdmin)

admin.site.site_title = 'Управление блогом'
admin.site.site_header = 'Управление блогом'
