from django import forms
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from disaster.models import DisasterReport
from .models import Disaster

@login_required
class ReportDisasterForm(forms.Form):
    def clean_disaster_report(self):#meant to clean the data from the form
        data=self.cleaned_data['casualties']
        data.self.cleaned_data['costOfDamages']
        
        #we want to make sure that casualties and cost of damages are integers
        if data.is_integer():
            return data

        else:
            raise ValidationError(_('Value should be a whole number'))

    
    class Meta:
        model=DisasterReport
        fields=['reportSubject','description','casualties','costOfDamages']
        labels={
            'reportSubject': _('Report Title'),
            'disasterName': _('Disaster Name'),
            'description': _('Comprehensive report'),
            'casualties': _('Casualties'),
            'costOfDamages': _('Damage Cost'),
        }
        help_texts={
            'casualties': _('integer values!'),
            'costOfDamages': _('integer values!'),
        }


class DisasterModelForm(ModelForm):
    class Meta:
        model=Disaster
        fields='__all__'

    minTemp=forms.IntegerField()
    maxTemp=forms.IntegerField()
    rainfall=forms.IntegerField()
    evaporation=forms.IntegerField()
    sunshine=forms.IntegerField()
    windGustDir=forms.IntegerField()
    windGustSpeed=forms.IntegerField()
    windDirEarly=forms.IntegerField()
    windDirLate=forms.IntegerField()
    windSpeedEarly=forms.IntegerField()
    windSpeedLate=forms.IntegerField()
    humidityEarly=forms.IntegerField()
    humidityLate=forms.IntegerField()
    pressureEarly=forms.IntegerField()
    pressureLate=forms.IntegerField()
    cloudEarly=forms.IntegerField()
    cloudLate=forms.IntegerField()
    rainToday=forms.IntegerField()