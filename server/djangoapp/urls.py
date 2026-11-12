from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='get_dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('get_dealers', views.get_dealers, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealers, name='get_dealers_by_state'),
    path('get_cars', views.get_cars, name='get_cars'),
    path('add_review', views.add_review, name='add_review'),
    path('getallcar', views.getallcarmakes, name='getallcarmakes'),
    path('getallcarmakes', views.getallcarmakes, name='getallcarmakes'),
]
