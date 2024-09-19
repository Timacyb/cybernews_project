from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import News, Category
from .forms import ContactForm


def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    # news_list = News.objects.all()
    context = {
        "news_list": news_list
    }

    return render(request, "news/news_list.html", context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)

    context = {
        "news": news
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
        context['news_list'] = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:5]
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
