from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.hello),
    path('upload',views.upload),
    path('gallery',views.gallery),
    path('<hash_id>',views.viewimg),


]
