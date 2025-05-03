from django.db import models

class HealthCard(models.Model):
    PUBLISH_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('SMS', 'Short Messaging Service'),
        ('MMS', 'Multimedia Message'),
    ]
    
    farmer_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    ec = models.FloatField(blank=True, null=True)
    oc = models.FloatField(blank=True, null=True)
    n = models.FloatField(blank=True, null=True)
    p = models.FloatField(blank=True, null=True)
    k = models.FloatField(blank=True, null=True)
    b = models.FloatField(blank=True, null=True)
    s = models.FloatField(blank=True, null=True)
    zn = models.FloatField(blank=True, null=True)
    cu = models.FloatField(blank=True, null=True)
    fe = models.FloatField(blank=True, null=True)
    mn = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.CharField(max_length=20, choices=PUBLISH_CHOICES, default='WhatsApp', blank=True, null=True)

    def __str__(self):
        return self.farmer_name if self.farmer_name else "Unnamed Health Report"
