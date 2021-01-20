from django.db import models

# Create your models here.

class Devices(models.Model):

    primary   = models.AutoField(primary_key=True)
    name      = models.CharField(max_length=300, default='No Item')
    ipaddress = models.CharField(max_length=300, default='No Item')

    def __unicode__(self):
        return self.primary

    class Meta:
        ordering = ('primary',)
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return str('{0} : {1}'.format(
            self.name,
            self.ipaddress))
