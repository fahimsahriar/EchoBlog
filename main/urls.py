from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('post/all/', views.post_list, name='post_list'),
    #path('post/<int:pk>/edit/', views.update_post, name='update_post'),
    #path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('user/new/', views.new_user, name='new_user'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('search/', views.search_posts, name='search_posts'),
]