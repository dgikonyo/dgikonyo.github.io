from django import forms
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from disaster.models import DisasterReport
from .models import Disaster
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class DisasterModelForm(forms.Form):
    class Meta:
        model=Disaster
        fields='__all__'

    Sunshine=forms.IntegerField()
    Humidity9am=forms.IntegerField()
    Humidity3pm=forms.IntegerField()
    Pressure9am=forms.IntegerField()
    Pressure3pm=forms.IntegerField()
    Cloud9am=forms.IntegerField()
    Cloud3pm=forms.IntegerField()
    Temp9am=forms.IntegerField()
    Temp3pm=forms.IntegerField()
    RainToday=forms.IntegerField()
    RISK_MM=forms.IntegerField()


#registration form
class NewUserForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=("username","email","password1","password2")

    def save(self, commit=True):
        user=super(NewUserForm,self).save(commit=False)
        user.email=self.cleaned_data['email']

        if commit:
            user.save()
        return user