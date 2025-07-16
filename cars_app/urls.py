from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('add/', views.add_car, name='add_car'),
    path('list/', views.car_list, name='car_list'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('logout/', views.logout_view, name='logout'),
]

# هذا السطر خارج قائمة urlpatterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

