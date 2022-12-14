from django.urls import path, include

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('api-auth/', include('rest_framework.urls')),
    path('competitions/', views.competitions_list),
    path('competitions/add/', views.competitions_add),
    path('competitions/<int:pk>/', views.competitions_detail),
    path('competitions/<int:pk>/delete/', views.competitions_delete),
    path('competitions/<int:pk>/update/', views.competitions_update),
    path('user-detail/<str:username>/add/', views.user_details_add),
    path('registrations/', views.registrations_list_of_all_users),
    path('registrations/status/<str:state>/', views.registrations_list_by_status),
    path('registrations/<str:username>/add/', views.registrations_add),
    path('registrations/<str:username>/', views.registrations_list),
    path('registrations/<str:username>/<int:pk>/', views.registrations_detail),
    path('registrations/<int:pk>/change/', views.registrations_change_status),
    path('register/', views.RegisterView.as_view()),
]