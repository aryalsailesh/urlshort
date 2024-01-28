from django.db import models

# Create your models here.


#url shortener model  
class UrlShortener(models.Model):
    short_url = models.CharField(max_length=100)
    long_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.short_url