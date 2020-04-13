from django.db import models

# Create your models here.
class Record(models.Model):
    hash = models.CharField(max_length=200,default='',unique=True)
    faces = models.CharField(max_length=100,default='')
    facesNum=models.IntegerField(default=0)
    
    def __str__(self):
        return self.hash

    def save(self):
        a=self.faces
        self.facesNum=len(a.strip('[]').strip('()').split('), ('))
        super(Record, self).save()

        