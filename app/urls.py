from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

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
    
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)