from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'windowstest.views.home', name='home'),
    # url(r'^windowstest/', include('windowstest.foo.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'windowstest.core.views.index'),
    (r'^add/$', 'windowstest.core.views.add_todo'),
    (r'^test/$', 'windowstest.core.views.test_path'),
)
