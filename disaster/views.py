from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import User,DisasterReport,Disaster

"""Index is a function used in rendering the details to be included
in the index.html file"""
def index(request):
    """view function for home page of site"""

    #generate a list of all disasters
    floodEvent=DisasterReport
    floodLocations=DisasterReport.objects.filter(validated=True).count()
    num_floods=DisasterReport.objects.count()
    #will give a count of all possible number of floods expected

    context={
        'floodEvent':floodEvent,
        'floodLocations':floodLocations,
        'num_floods':num_floods,
    }
    #render the html template index.html with data in the context variable
    return render(request, 'index.html',context=context)

"""The class is used to generate a list of all alerts that have been validated
"""
class DisasterListView(generic.ListView):
    model=DisasterReport
    context_object_name='alerts_list'#is the name of the list
    template_name='disaster/index.html'#is the target html file that will have the alerts

    def get_queryset(self):
        #list upto five validated alertss
        return DisasterReport.objects.filter(validated=True)[:5]

class DisasterDetailView(generic.DetailView):
    