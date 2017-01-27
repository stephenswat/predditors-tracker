from django.db import models

# Create your models here.
class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(db_index=True, unique=True, max_length=64)

    def __str__(self):
        return self.name

class Constellation(models.Model):
    id = models.IntegerField(primary_key=True)
    region = models.ForeignKey(Region, related_name='constellations', db_index=True)
    name = models.CharField(db_index=True, unique=True, max_length=64)

    def __str__(self):
        return self.name

class SolarSystem(models.Model):
    id = models.IntegerField(primary_key=True)
    constellation = models.ForeignKey(Constellation, related_name='systems', db_index=True)
    name = models.CharField(db_index=True, unique=True, max_length=64)

    security = models.FloatField()

    def __str__(self):
        return self.name

class ItemType(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.IntegerField(db_index=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    volume = models.DecimalField(max_digits=25, decimal_places=5)

    def __str__(self):
        return self.name
