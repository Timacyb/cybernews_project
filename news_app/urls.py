from django.urls import path
from .views import news_list, news_detail, homePageView, ContactPageView, errorPageView, HomePageView, \
    KiberSportView, CtfViews, TexnologiyalarViews, KiberjinoyatlarViews

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('contact-us/', ContactPageView.as_view(), name="contact_page"),
    path('404/', errorPageView, name="404_page"),
    path('cybersport/', KiberSportView.as_view(), name='cybersport_news_page'),
    path('ctf/', CtfViews.as_view(), name='ctf_news_page'),
    path('texnologiyalar/', TexnologiyalarViews.as_view(), name='texnologiyalar_news_page'),
    path('kiberjinoyatlar/', KiberjinoyatlarViews.as_view(), name='kiberjinoyatlar_news_page')
]
