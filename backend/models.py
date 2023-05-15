from django.db import models

class Exemplar(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=80)
    exemplar = models.CharField(max_length=255)
    area = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name