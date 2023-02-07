from . import views
from django.urls import path

app_name = 'box'

urlpatterns = [
	path('',views.MainView.as_view(), name ="main"),
	path('opening/', views.OpeningView.as_view(), name="opening"),
	path('notify', views.AddNotificationView.as_view(), name="notify"),
	path('signup', views.SignupView.as_view(), name="signup"),
	path('unsubscribe/<product__name>', views.remove_notification, name="nopeify")
]