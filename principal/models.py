from django.db import models

# Create your models here.

class Bebida(models.Model):
		nombre = models.CharField(max_length=50)
		ingredientes = models.TextField()
		preparacion = models.TextField()

		def __unicode__(self):
			return self.nombre