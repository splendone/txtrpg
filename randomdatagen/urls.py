from django.conf.urls import patterns, include, url
from django.contrib import admin
from hamals import views

#urlpatterns = patterns('',
    #url(r'^hamals/', 'hamals.views.checkSignature', name='checkSignature'),
    #url(r'^hamalstest/', 'hamals.views.test', name='test'),
    #url(r'^admin/', include(admin.site.urls)),
#)
urlpatterns = [
    url(r'^hamals/', views.checkSignature),
#    url(r'^hamalstest/', views.test),
    url(r'^fc/', views.fc),
    url(r'^admin/', admin.site.urls),
]
