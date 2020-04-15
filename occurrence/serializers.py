from rest_framework import serializers
from .models import Occurrence


class OccurrenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Occurrence
        fields = '__all__'

class OccurrenceSerializerPost(serializers.ModelSerializer):
    # define dos campos do objeto que sera apresentado, mas limita a 
    #   edicao de author, location e status
    class Meta:
        model = Occurrence
        fields = (
        	'category_of_occur', 'description', 'address',
            'location', 'author','status','date_creation',
            'date_update',
        	)
        read_only_fields = ('location','author','status')

class OccurrenceSerializerPut(serializers.ModelSerializer):
    # define dos campos do objeto que sera apresentado, mas limita a 
    #   edicao de author e location
    
    class Meta:
        model = Occurrence
        fields = (
        	'category_of_occur', 'description', 'address',
            'location', 'author','status','date_creation',
            'date_update',
        	)
        read_only_fields = ('location','author',)
