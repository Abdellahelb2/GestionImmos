from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from .views import BienUpdateView, BienDeleteView

urlpatterns = [
    path('', views.SayHello, name='SayHello'),
    path('about/', views.Settings, name='Settings'),
    path('service/', views.Said, name='Services'),
    path('contact/', views.Con, name='Contact'),
    path('login/', views.Loginpage, name='Loginpage'),
    path('registeruser/',views.Register,name='Register'),
    path('main/',views.main,name='main'),
    path('logout/',views.logout,name='logout'),
    path('login/', views.Loginpage, name='Loginpage'),
    path('<int:id>',views.product_detail,name='Product' ),
    path('product/',views.product_list,name='Products'),
    path('Product/add/', views.add_product, name='AddProduct'),
    path('modify-profile/', views.modify_profile, name='modify_profile'),
    path('profile/', views.profile, name='profile'),
    path('dash/', views.dash, name='Dashboard'),
    path('messaging/<int:bien_id>/<int:recipient_id>/', views.conversation, name='conversation'),
    path('inbox/', views.inbox, name='inbox'),
    path('favoris/add/<int:bien_id>/', views.add_to_favoris, name='add_to_favoris'),
    path('favoris/remove/<int:bien_id>/', views.remove_from_favoris, name='remove_from_favoris'),
    path('mes-favoris/', views.my_favoris, name='my_favoris'),
    path('bien/<int:pk>/modifier/', BienUpdateView.as_view(), name='bien_modifier'),
    path('bien/<int:pk>/supprimer/', BienDeleteView.as_view(), name='bien_supprimer'),
    path('reservation/<int:reservation_id>/<str:action>/',views.traiter_reservation, name='traiter_reservation'),
    path('reservations/gestion/', views.dashboard_entrepreneur, name='dashboard_entrepreneur'),
    path('bien/<int:bien_id>/status/', views.update_bien_status, name='update_bien_status'),
    path('update-bien/<int:id>/', views.update_bien_status, name='update_bien_status'),





]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)