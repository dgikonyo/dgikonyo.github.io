from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),#views.index is a function called index() in the views.py file
    path('alerts/',views.DisasterListView.as_view(),name='alerts'),
    path('alerts/<int:pk',views.DisasterDetailView.as_view(),name='alert_detail'),

]

