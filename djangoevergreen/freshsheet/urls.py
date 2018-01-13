# from django.conf.urls import url
#
# from . import views
#
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
# ]

from django.urls import path
from django.conf.urls import url

from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:id>/', views.details, name='details'),
    path('cart/', views.cart, name='cart'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]
