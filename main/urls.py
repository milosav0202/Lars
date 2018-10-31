from django.conf.urls import patterns, url, include

from main import views
import django.contrib.auth.views as djauthviews

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^sync$', views.sync, name='sync'),
    url(r'^accounts/login/$', djauthviews.login, name="login", kwargs={'template_name': 'main/login.mko'}),
    url(r'^accounts/logout/$', djauthviews.logout_then_login, name="logout"),
    url(r'^ajax/buildReports/$', views.ajax_generateReportSet, name="buildReports"),

)


# urlpatterns += patterns('django.contrib.auth.views',
#     (r'^accounts/logout/$', 'logout_then_login'),
# )
 
# # this then comes after
# urlpatterns += patterns('',
#     #(r'^accounts/profile/$', profile_page),
#     (r'^accounts/', include('registration.backends.default.urls')),
# )

# from django.contrib.auth import logout

# def logout_view(request):
#     logout(request)