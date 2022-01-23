from django.urls import path
from . import views

'''
    the HTML page is referred to using the 'name' attribute
'''

urlpatterns = [
    path('',views.index,name='index'),#views.index is a function called index() in the views.py file
    path('alerts/',views.DisasterListView.as_view(),name='alerts'),
    path('alerts/<int:pk>',views.DisasterDetailView.as_view(),name='disasterreport_detail'),#<int:pk> will capture the disaster id
    path('alerts/create/', views.ReportCreate.as_view(), name='disasterreport_form'),
    path('status/',views.FormView,name='status'),
    path('form/',views.FormView,name='FormView'),
    path('contact/',views.contactUs,name='constactUs'),
    path("register",views.register_request,name="register"),
]

