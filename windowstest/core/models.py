from django.db import models

# Create your models here.
class todo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default = "")
    created = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.name  
        
