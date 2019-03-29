
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^account/', include('account.urls', namespace='account', app_name='account')),
    url(r'^password/', include('password_reset.urls', namespace='pwd_reset', app_name='pwd_reset')),
    url(r'^article/', include('article.urls', namespace='article', app_name='article')),
    url(r'home/', TemplateView.as_view(template_name='home.html'), name='home'),
]
