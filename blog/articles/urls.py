from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *
from .api.views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', cache_page(10)(index), name='home'),
    path('blog/', ArticlesView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', detail, name='view_article'),
    path('blog/search/', Search.as_view(), name='search'),
    path('blog/action_search/', action_search, name='action_search'),
    path('blog/contacts/', contacts, name='contacts'),
    path('blog/about/', about, name='about'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('api/', ArticleListView.as_view(), name='api'),
    path('api/<int:pk>/', ArticleDetailView.as_view(), name='apiDetail'),
]