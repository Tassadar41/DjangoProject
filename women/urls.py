from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page
from rest_framework import routers

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

# class MyCustomRouter(routers.SimpleRouter):
#     routers = [
#         routers.Route(
#             url=r'^{prefix}$',
#             mapping={'get': 'list',},
#             name='{basename}-list',
#             detail=False,
#             initkwargs={'suffix': 'List'}
#         ),
#         routers.Route(
#             url=r'^{prefix}{lookup}$',
#             mapping={'get': 'retrieve'},
#             name='{basename}-list',
#             detail=True,
#             initkwargs={'suffix': 'Detail'}
#         )
#     ]


#router = routers.DefaultRouter()
#router = routers.SimpleRouter()
#router = MyCustomRouter()
#router.register(r'women', WomenViewSet, basename='women')




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
    path('captcha/', include('captcha.urls')),

    path('api/v1/womenlist/', WomenAPIView.as_view()),
    path('api/v1/womenlist/<int:pk>/', WomenAPIView.as_view()),


    path('api/v1/womenlistmodel/', WomenAPIList.as_view()),
    path('api/v1/womenlistmodel/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womenlistmodel/delete/<int:pk>/', WomenAPIDestroy.as_view()),
    path('api/v1/womendetail/<int:pk>/', WomenAPIDetailView.as_view()),

    # path('api/v1/womenlistmodel/', WomenViewSet.as_view({'get': 'list'})),
    # path('api/v1/womenlistmodel/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),
    #path('api/v1/womenlistmodel/<int:pk>/', WomenAPIList.as_view()),
    # path('api/v1/', include(router.urls)), #http://127.0.0.1:8000/api/v1/women

    path('api/v1/drf-auth/', include('rest_framework.urls')),

    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]