from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
#from django.contrib.auth.mixins import LoginRequiredMixin


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
from sklearn.externas import joblib
import pandas as pd 
from django.shortcuts import render, redirect 
from django.contrib import messages 

# Create your views here.
from .models import User,DisasterReport,Disaster
from .forms import DisasterModelForm
from .serializers import DisasterSerializer

#will be used for the form
from disaster.forms import ReportDisasterForm

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

@api_view(["POST"])#is a decorator, will handle the post requests
def disasterreject(request):#this is a view
    try:
        mdl=joblib.load("/home/gikonyo/Public/Personal/Projects/django_stuff/tujue/disaster/weatherModel.pkl")
        mydata=request.data
        unit=np.array(list(mydata.values()))
        unit=unit.reshape(1,-1)
        scalers=joblib.load("/home/gikonyo/Public/Personal/Projects/django_stuff/tujue/disaster/weatherModel.pkl")
        X=scalers.transform(unit)
        y_pred=mdl.predict(X)
        newdf=pd.DataFrame(y_pred)
        newdf=newdf.replace({1:'rain',0:'no rain'})
        return JsonResponse('Tomorrow we have predicted {}'.format(newdf),safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)