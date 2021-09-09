# serializers.py
from rest_framework import serializers
from .models import Allproduct

class AllproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allproduct #มาจากmodel ไหน
        fields = ('id','catname','name','price','detail','quantity')

