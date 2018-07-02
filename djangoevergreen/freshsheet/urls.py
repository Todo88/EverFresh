# from django.conf.urls import url
#
# from . import views
#
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
# ]
from django.contrib.auth.views import logout
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:item_pk>/<int:quantity>/', views.add_to_cart_view, name='add_to_cart'),
    path('add_line_items_to_cart/', views.add_line_items_to_cart, name="add_line_items_to_cart"),
    path('remove_from_cart/<int:line_item_pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('invoice/<int:order_pk>/', views.invoice, name='invoice'),
    path('accounts/', include('registration.backends.default.urls')),
    path('accounts/registration_request', views.RequestAccountCreateView.as_view(), name='registration_request'),
    path('thanks/', views.thanks, name='thanks'),

    # Logout and nicely redirect, normal logout does not redirect
    url(r'logout/', logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),

    path('freshsheets/', views.list_freshsheets, name='list_freshsheets'),
    path('freshsheets/details/<int:id>/', views.details, name='detail_freshsheet'),
    path('freshsheets/create/', views.FreshSheetCreateView.as_view(), name="create_freshsheet"),
    path('freshsheets/edit/<int:pk>', views.FreshSheetUpdateView.as_view(), name="edit_freshsheet"),
    path('freshsheets/delete/<int:pk>', views.FreshSheetDeleteView.as_view(), name="delete_freshsheet"),
    path('freshsheets/publish/<int:pk>', views.publish, name="publish_freshsheet"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]
