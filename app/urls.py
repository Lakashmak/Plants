from django.urls import path
from .views import catalog, product_page, basket, search, registration, personal_area, login_page, info, checkout_page, order_list

urlpatterns = [
    path('', catalog, name='home'),
    path('product_page/<int:id>/', product_page, name='product_page'),
    path('basket/', basket, name='basket'),
    path('search/', search, name='search'),
    path('registration/', registration, name='registration'),
    path('personal_area/', personal_area, name='personal_area'),
    path('login_page/', login_page, name='login_page'),
    path('info/<str:massange>/', info, name='info'),
    path('checkout_page/', checkout_page, name='checkout_page'),
    path('order_list/', order_list, name='order_list'),
]