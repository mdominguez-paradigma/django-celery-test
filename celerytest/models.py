from django.db import models
from django.core.validators import RegexValidator


class SimpleEntry(models.Model):
    body = models.TextField()

class SimpleUser(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=9, 
        validators=[RegexValidator(r'\d{9}')]
    )
    # Para simplificar en el ejemplo la semana es un entero
    # con la semana de gestación
    week = models.IntegerField() 
    risky = models.BooleanField()
    multiple = models.BooleanField()

    def __unicode__(self):
        return self.name

class Condition(models.Model):
    field = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return "{0} = {1}".format(self.field, self.value)

class ContentProducer(models.Model):
    text_body = models.CharField(max_length=160)
    conditions = models.ManyToManyField(Condition) 
    
    def __unicode__(self):
        return self.text_body[:50] 
