from django.urls import path
from . import views

app_name = 'mailMagazine'
urlpatterns = [
    path('', views.SubscribedUserCreateView.as_view(), name='index'),
    path('complete', views.SubscribedUserCreateCompleteView.as_view(), name='complete')
]