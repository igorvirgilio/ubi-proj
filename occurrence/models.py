
from django.contrib.gis.db import models

# Create your models here.
class Occurrence(models.Model):
	# Definicao das categorias de ocorrencia
	CONSTRUCTION = 'Construction'
	SPECIAL_EVENT = 'Special Event'
	INCIDENT = 'Incident'
	WEATHER_CONDITION = 'Weather Condition'
	ROAD_CONDITION = 'Road Condition'

	TYPE_OF_OCCUR_CHOICES = [
    	(CONSTRUCTION, 'Construction'),
    	(SPECIAL_EVENT, 'Special Event'),
    	(INCIDENT, 'Incident'),
    	(WEATHER_CONDITION, 'Weather Condition'),
    	(ROAD_CONDITION, 'Road Condition'),
    ]

	# Definicao dos possiveis status da ocorrencia
	VALIDADO = 'Validado'
	POR_VALIDAR = 'Por Validar'
	RESOLVIDO = 'Resolvido'
	
	TYPE_OF_STATUS = [
		(POR_VALIDAR, 'Por validar'),
		(VALIDADO, 'Validado'), 
		(RESOLVIDO, 'Resolvido'),
	]
	
	category_of_occur 	= models.CharField(max_length=17,choices=TYPE_OF_OCCUR_CHOICES,)
	description 		= models.TextField(blank=False, null=True) 
	address				= models.TextField(blank=False, null=True)
	location			= models.PointField(blank=False, null=True) 
	author				= models.TextField() # estara associado com o utilizador que estiver autenticado
	date_creation		= models.DateTimeField(auto_now_add=True)
	date_update			= models.DateTimeField(auto_now=True)
	status				= models.CharField(max_length=11,choices=TYPE_OF_STATUS,default=POR_VALIDAR,)
	

	def __str__(self):
		return self.category_of_occur
	