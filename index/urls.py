from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.hello),
    path('uploadImage',views.uploadImage),
    path('gallery',views.gallery),
    path('upload',views.upload),
    path('<hash_id>',views.viewimg),


]
