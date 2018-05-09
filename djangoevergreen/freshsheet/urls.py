# from django.conf.urls import url
#
# from . import views
#
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
# ]

from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('details/<int:id>/', views.details, name='details'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:item_pk>/<int:quantity>/', views.add_to_cart_view, name='add_to_cart'),
    path('add_line_items_to_cart/', views.add_line_items_to_cart, name="add_line_items_to_cart"),
    path('remove_from_cart/<int:line_item_pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('invoice/<int:order_pk>/', views.invoice, name='invoice'),
    path('^accounts/', include('registration.backends.default.urls')),
    path('create_freshsheet/', views.create_freshsheet, name="create_freshsheet")
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]
