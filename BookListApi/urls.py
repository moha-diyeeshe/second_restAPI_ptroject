from django.urls import path
from . import views


from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-item',views.menu_item),
    path('menu-item/<int:pk>', views.Single_item),
    path('secret/',views.secret),
    path('manager-view/',views.manager_view),
    path('throttle-check/',views.throttle_check),
    path('throttle-check-auth/',views.throttle_check_auth),
    path('api-auth-token',obtain_auth_token)


]