
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('show_post/<int:id>/', views.show_post, name='show_post'),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
    path('make_post/', views.make_post, name='make_post'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
