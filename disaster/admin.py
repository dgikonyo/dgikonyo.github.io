from django.contrib import admin

# Register your models here.
from .models import User, Disaster,DisasterReport
# Changing the site headers
admin.site.site_header = "Tujue"
admin.site.site_title="Tujue"
admin.site.index_title="Tujue"
admin.site.register(User)
admin.site.register(Disaster)
#admin.site.register(DisasterReport)

@admin.register(DisasterReport)
class DisasterReportAdmin(admin.ModelAdmin):
    list_display=('disasterName','dateCreated','reportID','country','casualties')

   