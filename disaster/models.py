from django.db import models
import uuid
from .country import countryList
from django.urls import reverse


# Create your models here.
class User(models.Model):
    userID=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    firstName=models.CharField(max_length=30,help_text='First name')
    lastName=models.CharField(max_length=30,help_text='Last name')
    emailAddress=models.EmailField(max_length=254,)
    phoneNumber=models.IntegerField(help_text='Phone Number')
    address=models.IntegerField(help_text='Address')
    country=models.CharField(max_length=20,choices=countryList)
    city=models.CharField(max_length=20,help_text='City')
    dateCreated=models.DateTimeField(auto_now_add=True)#will add the user record upon account creation


    def __str__(self):
        return self.emailAddress
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this 
          User."""
        return reverse('user', args=[str(self.userID)])

class Disaster(models.Model):
    disasterID=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)#This ley can't be edited
    minTemp=models.CharField('Minimum Temperature',max_length=20)
    maxTemp=models.CharField('Maximum Temperature',max_length=20)
    rainfall=models.CharField('Rainfall',max_length=20)
    evaporation=models.CharField('Evaporation',max_length=20)
    sunshine=models.CharField('Sunshine',max_length=20)
    windGustDir=models.CharField('Wind Gust',max_length=20)
    windGustSpeed=models.CharField('WindGustSpeed',max_length=20)
    windDirEarly=models.CharField('Wind Direction 9 AM',max_length=20)
    windDirLate=models.CharField('Wind Direction 3 PM',max_length=20)
    windSpeedEarly=models.CharField('Wind Speed 9 AM',max_length=20)
    windSpeedLate=models.CharField('Wind Speed 3 PM',max_length=20)
    humidityEarly=models.CharField('Humidity 9 AM',max_length=20)
    humidityLate=models.CharField('Humidity 3 PM',max_length=20)
    pressureEarly=models.CharField('Pressure 9 AM',max_length=20)
    pressureLate=models.CharField('Pressure 3 PM',max_length=20)
    cloudEarly=models.CharField('Cloud 9 AM',max_length=20)
    cloudLate=models.CharField('Cloud 3 PM',max_length=20)
    rainToday=models.CharField('Rain Today',max_length=20)

    
    def __str__(self):
        return self.rainToday

    def get_absolute_url(self):
        """Returns the url to access a detail record for this 
          Disaster."""
        return reverse('disaster', args=[str(self.disasterID)])

    
class DisasterReport(models.Model):
    #Fields
    reportID=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    reportSubject=models.CharField('Report Title',max_length=20,help_text='What are you reporting about?',default='')
    disasterChoices=(
        ('F','Flood'),
        ('E','EarthQuake'),
        ('L','Land slide'),
        ('W','Wild/Forest Fires')
    )
    disasterName=models.CharField(
        'Disaster Name',
        max_length=20,
        choices=disasterChoices
        )


    dateCreated=models.DateTimeField('Date',auto_now=False,auto_now_add=True)#will automatically enter the current date and can't be edited
    costOfDamages=models.DecimalField('Damage Cost',max_digits=20,decimal_places=0)
    country=models.CharField('Country',max_length=20,choices=countryList)
    description=models.TextField('Description')
    casualties=models.IntegerField('Casualties')
    #userID=models.ForeignKey(User, on_delete=models.CASCADE,editable=False)#this is foreignKey relation to the User
    validated=models.BooleanField(default=False)

    """"def get_absolute_url(self):
        #Returns the url to access a detail record for a specific disaster report.
        return reverse('alerts', args=[str(self.reportID)])"""
    
    def __str__(self):
        return self.reportSubject

    #This class will control the default ordering of records returned when you query the model type
    '''So the order of occurrence will be reversed and the newest record will appear first because of the (-)'''
    class Meta:
        ordering=['-dateCreated','disasterName']
