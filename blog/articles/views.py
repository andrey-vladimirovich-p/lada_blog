from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Article, Comment
from django.db.models import Q
from .forms import UserRegisterForm, UserLoginForm, ContactForm, GuestCommentForm, UserCommentForm

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from .utils import Weather


def index(request):
    article_first = Article.objects.filter(is_published=True).first()
    popular_articles = Article.objects.order_by('-views').filter(is_published=True)[0:3]
    weat, temp, cities = Weather.weat, Weather.temp, Weather.cities
    context = {
        'temp': temp, 'cities': cities, 'weat': weat,
        'article_first': article_first,
        'popular_articles': popular_articles,
    }

    return render(request, 'index.html', context)


class ArticlesView(ListView):
    template_name = 'blog_list.html'
    model = Article
    context_object_name = 'article'
    paginate_by = 4

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


def detail(request, pk):
    article = Article.objects.get(pk=pk, is_published=True)
    article.views = article.views + 1
    article.save()
    comments = Comment.objects.order_by('-id').filter(article=pk, is_active=True)[:10]
    initial = {'article': article.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        initial['email'] = request.user.email
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, 'Коментарий сохранен и будет добавлен после проверки!')
        else:
            form = c_form
            messages.success(request, 'Коментарий не добавлен')

    context = {'article': article, 'comments': comments, 'form': form}
    return render(request, 'view_article.html', context)


def action_search(request):
    return render(request, 'action_search.html',)


class Search(ListView):
    template_name = 'search.html'
    context_object_name = 'article'
    paginate_by = 4

    def get_queryset(self):
        return Article.objects.filter(Q(title__icontains=self.request.GET.get('search')) | Q(
            content__icontains=self.request.GET.get('search')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        context['search_title'] = self.request.GET.get('search')
        return context


def about(request):
    return render(request, 'about.html', )


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{} ({})'.format(cd['subject'], cd['email'])
            mail = send_mail(subject, form.cleaned_data['content'],
                             'your_email@yandex.ru', ['mail@mail.ru'],
                             fail_silently=True)
            if mail:
                messages.success(request, 'Сообщение успешно отправлено.')
                return redirect('contacts')
            else:
                messages.error(request, 'Ошибка отправки, попробуйте снова.')
        else:
            messages.error(request, 'Ошибка!')
    else:
        form = ContactForm()
    return render(request, 'contacts.html',  {'form': form})
