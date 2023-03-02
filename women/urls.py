from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [

    # path('', index, name='home'),  # http://127.0.0.1:8000/
    path('', cache_page(60)(WomenHome.as_view()), name='home'),
    #path('', WomenHome.as_view(), name='home'),
    path('cats/<int:catid>/', categories),  # http://127.0.0.1:8000/categories/
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
    path('about/', about, name='about'),
    #path('addpage/', addpage, name='add_page'),
    path('addpage/', addPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', show_category, name='category'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('captcha/', include('captcha.urls'))
]
