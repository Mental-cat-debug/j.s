from django.urls import path # type: ignore
from django.conf.urls.static import static # type: ignore
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('beta/', views.beta, name='beta'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('store/', views.store, name='store'),
    path('contact/', views.contact, name='contact'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) # type: ignore