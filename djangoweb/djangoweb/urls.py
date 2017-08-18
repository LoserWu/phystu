"""djangoweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""	
from django.conf.urls import url,include
import settings
from django.contrib import admin
from django.conf.urls.static import static
import phyion.views as ph
urlpatterns =[
    url(r'^admin/', admin.site.urls),
	url(r'^mail/',ph.Mail),
	url(r'^manage/(\S{1,50})',ph.Manage),
	url(r'^init/$',ph.Begin),
	url(r'^Home/$',ph.Home),
	url(r'^NewsList/$',ph.NewsList),
	url(r'^news/(\S{1,20})',ph.News),
	url(r'^ActivityList/$',ph.ActivityList),
	url(r'^activity/(\S{1,20})',ph.Activity),
	url(r'^ResourceList/$',ph.ResourceList),
	url(r'^section/(\S{1,20})',ph.Section),
	url(r'^uploadFile',ph.UploadFile),
	url(r'^download/(\S{1,40})$',ph.DownloadFile),
	]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

