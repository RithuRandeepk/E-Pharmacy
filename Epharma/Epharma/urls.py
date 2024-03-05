"""
URL configuration for Epharma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.contrib.auth.forms import PasswordChangeForm     
from django import forms     
from  app1.forms import  MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm                                                                                                                                                                                                                                                                                                         


urlpatterns = [

    path('admin/', admin.site.urls),

    path('',views.home,name="homepage"),
    path('home2',views.HomeView.as_view(),name="home2"),
    path('reg',views.Registration.as_view(),name='regpage'),
    path('loginpage',views.LoginView.as_view(),name='loginpage'),
    path('upload', views.upload_file, name='upload_file'),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('logout',auth_view.LogoutView.as_view(next_page='homepage'),name='logout'),


    path('prdtview/<slug:val>',views.ProductView.as_view(),name='prdtview'),
    path('product-detail/<int:pk>',views.Productdetail.as_view(),name='product-detail'),
    path('brandwise/<slug:val>',views.BrandwiseDisplay.as_view(),name='brandwise'),

    path('add-to-cart',views.add_to_cart,name="add-to-cart"),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    path('showwishlist',views.show_wishlist,name="showwishlist"),
    path('cart',views.show_cart,name="showcart"),
    path('search/',views.search,name="search"),
    path('checkout',views.checkout.as_view(),name="checkout"),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart,name='removecart'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.orders,name='orders'),



    path('profile',views.ProfileView.as_view(),name="profile"),
    path('address',views.address,name="address"),
    path('updateaddress/<int:pk>',views.Updateaddress.as_view(),name="updateaddress"),

   

    path('passwordchange',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset',auth_view.PasswordResetView.as_view(template_name='passord_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done',auth_view.PasswordResetDoneView.as_view(template_name='passord_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name='passord_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password-reset-complete',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete')






]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header="E-Pharma"
admin.site.site_title="E-Pharma"
admin.site.site_index_title=" Wlcome to E-Pharma"


