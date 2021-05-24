from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('recruit-students', views.RecruitStudentsTemplateView.as_view(), name='recruit_students'),
    path('common-orders', views.CommonOrdersTemplateView.as_view(), name='common_orders'),
    path('special-provision', views.SpecialProvisionsTemplateView.as_view(), name='special_provision'),
    path('fee', views.FeeTemplateView.as_view(), name='fee'),
    path('about', views.AboutTemplateView.as_view(), name='about'),
    path('review', views.ReviewTemplateView.as_view(), name='review'),
]
