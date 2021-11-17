from django.test import TestCase

from disaster.models import DisasterReport

# Create your tests here.
class DisasterReportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DisasterReport.objects.create(reportID='1e2142f2-30eb-4121-8e95-00ace2b8d749',reportSubject='Drought in Transmara',disasterName='Drought',
        costOfDamages=3,country='AW',description='uyvsducy6eevydevDKVCUD',casualties=4,validated=True)

    def test_report_subject_label(self):
        disasterReport=DisasterReport.objects.get()
        field_label=disasterReport._meta.get_field('reportSubject')
        self.assertEqual(field_label, 'Report Title')

    
  
