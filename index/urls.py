from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.hello),
    path('uploadImage',views.uploadImage),
    path('gallery',views.gallery),
    path('upload',views.uploadBlur),
    path('restore',views.uploadRestore),
    path('restoreimage',views.restore),
    path('<hash_id>',views.viewimg),
]
