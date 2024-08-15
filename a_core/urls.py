"""
URL configuration for a_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from a_posts import views
from a_users import views as u_views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path("category/<str:category>/", views.home_view, name="category"),
    path("post/create/", views.post_create_view, name="post_create"),
    path("post/delete/<str:id>/", views.post_delete_view, name="post_delete"),
    path("post/edit/<str:pk>/", views.post_edit_view, name="post_edit"),
    path("post/<str:pk>/", views.post_page_view, name="post"),
    path("post/like/<str:pk>/", views.like_post, name="like_post"),
    path("comment/like/<str:pk>/", views.like_comment, name="like_comment"),
    path("reply/like/<str:pk>/", views.like_reply, name="like_reply"),
    path("commentsent/<str:pk>/", views.comment_sent, name="comment_sent"),
    path("reply-sent/<str:id>/", views.reply_sent, name="reply_sent"),
    path("comment/delete/<str:id>/", views.comment_delete_view, name="comment_delete"),
    path("reply/delete/<str:id>/", views.reply_delete_view, name="reply_delete"),
    path("profile/", u_views.profile_view, name="profile"),
    path("<str:username>/", u_views.profile_view, name="userprofile"),
    path("profile/edit/", u_views.profile_edit_view, name="profile_edit"),
    path("profile/delete/", u_views.profile_delete_view, name="profile_delete"),
    path("profile/onboarding/", u_views.profile_edit_view, name="profile_onboarding"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
