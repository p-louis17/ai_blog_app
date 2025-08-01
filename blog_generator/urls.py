from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('login', views.user_login, name='login'),
#     path('signup', views.user_signup, name='signup'),
#     path('logout', views.user_logout, name='logout'),
#     path('generate-blog', views.generate_blog, name='generate-blog'),
#     path('blog-list', views.generate_list, name='blog-list'),
#     path('blog-details/<int:pk>/', views.blog_details, name='blog-details'),
#     path('home/', views.home, name='home'),
#     # path("instance/", views.instance_identifier, name="instance"),
# ]

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('generate-blog', views.generate_blog, name='generate-blog'),
    path('blog-list', views.generate_list, name='blog-list'),
    path('blog-details/<int:pk>/', views.blog_details, name='blog-details'),
]
