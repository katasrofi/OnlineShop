"""
URL configuration for OnlineShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings 
from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static 
from django.shortcuts import redirect
import traceback 
import os 

# Default home url 
def home_redirect(request):
    return redirect('base/', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', home_redirect),
]
# Automatic the url 
for app in settings.INSTALLED_APPS:
    try:
        app_name = app.split('.')[0]
        urls_path = os.path.join(app_name, 'urls.py')
        if os.path.exists(urls_path):
            urlpatterns.append(path(f'{app_name}/', include(f'{app_name}.urls')))
    except Exception as e:
        print(f'ERROR: Failed add urls {app}')
        print(f'Caused: {e.__class__.__name__} - {e}')
        print(f'Traceback:\n {traceback.format_exc()}')

# Set the media as main dir for uploaded image 
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)

