"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url 
from django.contrib import admin
from dashboard import views
from django.urls import path
"""
urlpatterns = [
    url('post/',views.post_view),
    url('feed/',views.feed_view),
    url('',views.signup_view),   
    url('login/',views.login_view),
    url('',views.home_view,name='home')
]
"""

urlpatterns = [
    url(r'^signup/$',views.signup_view,name='signup'),
    url(r'^feed/$',views.feed_view,name='feed'),
    url(r'^$',views.home_view,name='home'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'^like/$', views.like_view, name='like'),
    url(r'^comment/$',views.comment_view,name='comment'),
    url(r'^post/$', views.post_view, name='post'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^admin/', admin.site.urls),
]

"""if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""