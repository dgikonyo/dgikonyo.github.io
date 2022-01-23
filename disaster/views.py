from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view 
from django.core import serializers 
from rest_framework.response import Response 
from rest_framework import status 
from django.http import JsonResponse 
from rest_framework.parsers import JSONParser

import pickle
import json 
import numpy as np 
from sklearn import preprocessing 
from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd 
from django.shortcuts import render, redirect 
from django.contrib import messages 

# Create your views here.
from .models import User,DisasterReport,Disaster
from .forms import DisasterModelForm
from .serializers import DisasterSerializer

#will be used for the form
from disaster.forms import ReportDisasterForm
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

"""Index is a function used in rendering the details to be included
in the index.html file"""
@login_required
def index(request):

    
    """view function for home page of site"""

    #generate a list of all disasters
    floodEvent=DisasterReport
    floodLocations=DisasterReport.objects.filter(validated=True).count()
    num_floods=DisasterReport.objects.count()
    #will give a count of all possible number of floods expected

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context={
        'floodEvent':floodEvent,
        'floodLocations':floodLocations,
        'num_floods':num_floods,
        'num_visits': num_visits,
    }
    #render the html template index.html with data in the context variable
    return render(request, 'index.html',context=context)

def contactUs(request):
    return render(request,'contact.html')

def alerts(request):
    return render(request,'alerts.html')

"""The class is used to generate a list of all alerts that have been validated
"""
class DisasterListView(generic.ListView):
    model=DisasterReport
    context_object_name='disasterreport_list'#is the name of the list
    template_name='disaster/index.html'#is the target html file that will have the alerts

    def get_queryset(self):
        #list upto five validated alertss
        return DisasterReport.objects.filter(validated=True)[:5]#will print a maximum of five

class DisasterDetailView(generic.DetailView):#meant to show the specific details of a disaster(/disaster/<id>)
    model=DisasterReport
    #if a disaster doesn't exist, the class will generate a 404 error

class ReportCreate(CreateView):
    model=DisasterReport
    fields=['reportSubject','disasterName','description','casualties','costOfDamages']
    success_url = reverse_lazy('index')

#For querying the Form
class DisasterView(viewsets.ModelViewSet):
    queryset=Disaster.objects.all()#anytime I call the request, get all the values in the form
    serializer_class=DisasterSerializer


"""#@api_view(["POST"])#is a decorator, will handle the post requests
def disasterStatus(unit):#this is a view
    try:
        model=pickle.load(open("/home/gikonyo/Public/Personal/Projects/django_stuff/tujue/disaster/weatherModel_One.pkl","rb"))
        y_pred=model.predict(unit)
        newdf=pd.DataFrame(y_pred)     
        #newdf=newdf.replace({1:'rain',0:'no rain'})
        return newdf
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)"""

        
def FormView(request):
    if request.method=='POST':
        #form=DisasterModelForm(request.POST)
        #if form.is_valid():
        """Sunshine=form.cleaned_data['Sunshine']
        Humidity9am=form.cleaned_data['Humidity9am']
        Humidity3pm=form.cleaned_data['Humidity3pm']
        Pressure9am=form.cleaned_data['Pressure9am']
        Pressure3pm=form.cleaned_data['Pressure3pm']
        Cloud9am=form.cleaned_data['Cloud9am']
        Cloud3pm=form.cleaned_data['Cloud3pm']
        Temp9am=form.cleaned_data['Temp9am']
        Temp3pm=form.cleaned_data['Temp3pm']
        RainToday=form.cleaned_data['RainToday']
        RISK_MM=form.cleaned_data['RISK_MM']
        formDict=(request.POST).dict()  #will pick the POST data and saves it into a dictionary
        formList=list(formDict)
        formNp=np.array(formList)#form data converted to numpy array"""

        sunshine=request.POST["sunshine"]
        humidity9am=request.POST["humidity9am"]
        humidity3pm=request.POST["humidity3pm"]
        pressure9am=request.POST["pressure9am"]
        pressure3pm=request.POST["pressure3pm"]
        cloud9am=request.POST["cloud9am"]
        cloud3pm=request.POST["cloud3pm"]
        temp9am=request.POST["temp9am"]
        temp3pm=request.POST["temp3pm"]
        raintoday=request.POST["raintoday"]

        int_features=[int (x) for x in request.POST.values()]#will create a list called int_features

        formNp=[np.array(int_features)]#will form numpy array

        model=pickle.load(open("/home/gikonyo/Public/Personal/Projects/django_stuff/tujue/disaster/weatherModel_One.pkl","rb"))
        y_pred=model.predict(formNp)
        newdf=pd.DataFrame(y_pred)            
            
        
        prediction=newdf.replace({1:'Expecting rain tomorrow',0:'Expecting rain tomorrow'})
        
        if sunshine>="15" and humidity9am>="110" and humidity3pm>="100" and pressure9am>="1034":
            flood_alert="Expecting Flood"
        else:
            flood_alert="No Flood expected"


        context={
            #'newdf':newdf,
            'prediction':prediction,
            'flood_alert':flood_alert
        }
            

        return render(request,'disaster/status.html',context)#will redirect to status.html
            
    form=DisasterModelForm()

    return render(request,'disaster/disaster_form.html',{"form":form})

def register_request(request):
    if request.method== "POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            """username=request.POST["username"]
            email=request.POST["email"]
            password=request.POST["password"]
            password2=request.POST["password2"]

            registration_features=[x for x in request.POST.values()]"""
            user=form.save()
            login(request,user)
            messages.success(request,"Registration successful.")
            return render(request,'index.html')
        messages.error(request,"Unsuccessful registration.Invalid information.")

    form=NewUserForm()
    return render(request, 'registration/register.html', context={'register_form':form})
        




