from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', Index.as_view(), name='home'),     # cache_page(60)(Index.as_view())
    path('shop/', Shop.as_view(), name='shop'),
    path('blog/', blog, name='blog'),
    path('contacts/', contacts, name='contacts'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('shopping_cart/', shopping_cart, name='shopping_cart'),
    path('checkout/', checkout, name='checkout'),
    path('about/', about, name='about'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:category_slug>/', ShowCategory.as_view(), name='category'),
]