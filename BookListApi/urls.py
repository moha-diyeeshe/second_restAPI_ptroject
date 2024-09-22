from django.urls import path
from . import views

urlpatterns = [
    path('menu-item',views.menu_item),
    path('menu-item/<int:pk>', views.Single_item),

]