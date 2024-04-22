from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("all_posts/", views.all_posts, name="all_posts"),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path("profile/", views.profile, name="profile"),
    path("following/", views.following_posts, name="following_posts"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("post/<int:post_id>/unlike/", views.unlike_post, name="unlike_post"),
    path('user/<int:user_id>/', views.user_page, name='user_page'),
    path('admin/', admin.site.urls),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
]
