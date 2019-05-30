from django.urls import path

from . import views

app_name = 'proof'
urlpatterns = [
    path('sandbox/', views.sandbox, name='sandbox'),
    path('postulate/', views.postulate, name="postulate"),
    path('theorize/', views.theorize, name="theorize")
]
