from django.urls import path
from .views import order_list, order_create, order_edit, order_report, add_to_cart, view_cart, remove_from_cart, update_cart, checkout, order_success
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('orders/', order_list, name='order_list'),
    path('orders/create/', order_create, name='order_create'),
    path('orders/edit/<int:order_id>/', order_edit, name='order_edit'),
    path('orders/report/', order_report, name='order_report'),
    path('', views.index, name='index'),

    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order_success/', order_success, name='order_success'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)