from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import os

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'auth.views.login_user'),
    url(r'^login/', 'auth.views.login_user'),
    url(r'^logout/', 'auth.views.logout_user'),
    url(r'^register/', 'auth.views.register_user'),
    url(r'^home/', 'auth.views.homepage'),
    url(r'^UploadInfo/', 'UserInfo.views.UploadInfo'),
    url(r'^ViewUserInfo/', 'UserInfo.views.ViewUserInfo'), 
    url(r'^ViewUserStats/', 'SherlockStats.views.ViewUserStats'),
    url(r'^PlayGame/', 'SherlockGame.views.PlayGame'), 
    url(r'^PlayGameAnswer/', 'SherlockGame.views.PlayGameAnswer'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
)
