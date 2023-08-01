from django.urls import path
from . import views

urlpatterns = [
    path('', views.Compress.as_view(), name='compress'),
    path('convert/', views.Convert.as_view(), name='convert'),
    path('resize/', views.Resize.as_view(), name='resize'),
    path('create/', views.Create.as_view(), name='create'),
    path('download/<str:filename>/<path:save_path>/',views.Download.as_view() ,name='download')
]
