from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.utils import get_hitcount_model

from .models import News, Category
from .forms import ContactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser


def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    # news_list = News.objects.all()
    context = {
        "news_list": news_list
    }

    return render(request, "news/news_list.html", context)


from hitcount.views import HitCountDetailView, HitCountMixin


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active = True)
    comment_count = comments.count()

    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "comment_count": comment_count
    }

    return render(request, 'news/news_detail.html', context)


def homePageView(request):
    categories = Category.objects.all()
    news_list = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:5]
    cybersport_news_one = News.objects.filter(status=News.Status.Published, category__name='KiberSport').order_by(
        '-publish_time')[:1]
    cybersport_news = News.objects.filter(status=News.Status.Published, category__name='KiberSport').order_by(
        '-publish_time')[1:6]
    context = {
        'news_list': news_list,
        'categories': categories,
        'cybersport_news_one': cybersport_news_one,
        'cybersport_news': cybersport_news
    }

    return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:4]
        # context['cybersport_news_one'] = News.objects.filter(status=News.Status.Published,
        #                                                      category__name='KiberSport').order_by('-publish_time')[:1]
        context['kibersport_xabarlar'] = News.objects.filter(status=News.Status.Published,
                                                             category__name='KiberSport').order_by('-publish_time')[:5]
        context['ctf'] = News.objects.filter(status=News.Status.Published,
                                             category__name='CTF').order_by('-publish_time')[:5]
        context['kiberjinoyatlar'] = News.objects.filter(status=News.Status.Published,
                                                         category__name='KiberJinoyatchilik').order_by('-publish_time')[
                                     :5]
        context['texnologiyalar'] = News.objects.filter(status=News.Status.Published,
                                                        category__name='Texnologiyalar').order_by('-publish_time')[:5]
        return context


# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur </h2>")
#
#     context = {
#         "form": form
#     }
#
#     return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur!</h2>")
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)


def errorPageView(request):
    context = {

    }

    return render(request, 'news/404.html', context)


class KiberSportView(ListView):
    model = News
    template_name = 'news/kibersport.html'
    context_object_name = 'kibersportnews'

    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='KiberSport')
        # news = self.model.published.all().filter(category__name='KiberSport')
        return news


class CtfViews(ListView):
    model = News
    template_name = 'news/ctf.html'
    context_object_name = 'ctfnews'

    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='CTF')
        # news = self.model.published.all().filter(category='CTF')
        return news


class TexnologiyalarViews(ListView):
    model = News
    template_name = 'news/texnologiyalar.html'
    context_object_name = 'texnologiyalarnews'

    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='Texnologiyalar')
        # news = self.model.published.all().filter(category='Texnologiyalar')
        return news


class KiberjinoyatlarViews(ListView):
    model = News
    template_name = 'news/kiberjinoyatlar.html'
    context_object_name = 'kiberjinoyatlarnews'

    def get_queryset(self):
        news = News.objects.filter(status=News.Status.Published, category__name='KiberJinoyatchilik')
        # news = self.model.published.all().filter(category='KiberJinoyatchilik')
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'image')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru', 'slug',
              'body', 'body_uz', 'body_en', 'body_ru', 'image',
              'category', 'status')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
