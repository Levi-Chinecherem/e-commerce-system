from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrement-quantity/<int:item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('increment-quantity/<int:item_id>/', views.increment_quantity, name='increment_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('create-paystack-transaction/', views.create_paystack_transaction, name='create_paystack_transaction'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-error/', views.payment_error, name='payment_error'),
    path('payment-canceled/', views.payment_canceled, name='payment_canceled'),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
