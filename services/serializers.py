from rest_framework import serializers
from .models import Brochure

class BrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brochure
        fields = ['id', 'pdf', 'created_on', 'updated_on']


        
