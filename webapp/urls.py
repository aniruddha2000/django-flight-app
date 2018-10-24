from django.urls import path
from webapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path("<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book, name="book"),
    path("<int:flight_id>/cancle", views.cancle, name="cancle"),
]