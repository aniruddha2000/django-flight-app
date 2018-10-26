from django.urls import path
from webapp import views

app_name = "webapp"
urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('home', views.index, name="index"),
    path("<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book, name="book"),
    path("<int:flight_id>/cancle", views.cancle, name="cancle"),
]