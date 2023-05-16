from django.db import models

class Exemplar(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=80)
    exemplar = models.CharField(max_length=255)
    area = models.CharField(max_length=20)
    reservado = models.BooleanField(default=False)

    def as_json(self):
        return dict(
            id=self.id, 
            titulo=self.titulo,
            autor=self.autor, 
            exemplar=self.exemplar,
            area=self.area,
            reservado=self.reservado)
    