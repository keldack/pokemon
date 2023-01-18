from rest_framework import serializers
from catalog.models import Type, Pokemon


class TypeSimpleSerializer(serializers.ModelSerializer):

    class Meta:

        model = Type
        fields = ["name"]


class PokemonSimpleSerializer(serializers.ModelSerializer):

    types = TypeSimpleSerializer(many=True, read_only=True)
    #types = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Pokemon
        fields= ["poke_id", "name", "url", "types"]
        
        