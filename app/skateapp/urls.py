from django.urls import path, include

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('api-auth/', include('rest_framework.urls')),
    # path('druzynas/<int:pk>/czlonkowie', views.druzyna_czlonkowie_detail),s
    path('register/', views.RegisterView.as_view()),
]