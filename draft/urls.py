from django.urls import path
from . import views

app_name = 'draft'
urlpatterns = [
	path('lobby', views.lobby, name="lobby"),
	path('lobby/<str:room_name>/', views.asynclobby, name="alobby"),
	path('lobby/<str:room_name>/add', views.add_card, name="add_card")


]