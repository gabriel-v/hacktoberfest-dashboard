from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('contestants/', views.user_list),
    path('contestants/<str:username>/', views.user_info),
    path('events/', views.event_list),
    path('events_old/<int:event_id>/', views.event_info),
    path('events/<int:event_id>/', views.event_info2),
]

