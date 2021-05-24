from django.urls import path
from . import views

app_name = 'ec'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path('product/<int:pk>/order', views.OrderCreateView.as_view(), name='order'),
    path('product/order/complete', views.OrderCreateCompleteView.as_view(), name='complete'),
    path('product/order/failed', views.OrderCreateFailedView.as_view(), name='failed')
]
