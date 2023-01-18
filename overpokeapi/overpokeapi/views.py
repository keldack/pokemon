from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from catalog.models import Type, Pokemon, Feeder

# class LoginView(ObtainAuthToken):

#     def post(self, request, format=None):
        
#         data = request.data
#         user= authenticate(username=data["username"], password=data["password"])

#         return Response(
#             {"token": "OK"}
#         )


class AddGroupView(APIView):

    permission_classes = [IsAuthenticated]

    def post (self, request, type_id, format=None):

        print (f"Add group for '{type_id}'")

        feeder = Feeder.objects.get(pk=request.user.id)
        
        try:
            type_ = Type.objects.get(name=type_id)
        
            feeder.types.add(type_)
            feeder.save()

            return Response({
                "user": request.user.username,
                "types": [type_.name for type_ in feeder.types.all()]
            })
        except Type.DoesNotExist:
            return Response(
                {
                    "message": f"Unkown type '{type_id}' for pokemon category"
                },
                status=status.HTTP_404_NOT_FOUND
            )

class RemoveGroupView(APIView):

    permission_classes = [IsAuthenticated]

    def post (self, request, type_id, format=None):

        print (f"Remove group for '{type_id}'")

        feeder = Feeder.objects.get(pk=request.user.id)
        try:
            type_ = Type.objects.get(name=type_id)
        
            feeder.types.remove(type_)
            feeder.save()

            return Response({
                "user": request.user.username,
                "types": [type_.name for type_ in feeder.types.all()]
            })
        except Type.DoesNotExist:
            return Response(
                {
                    "message": f"Unkown type '{type_id}' for pokemon category"
                },
                status=status.HTTP_404_NOT_FOUND
            )

class UserMeView(APIView):

    permission_classes = [IsAuthenticated]

    def get (self, request, format=None):
        
        feeder = Feeder.objects.get(pk=request.user.id)

        return Response({
            "user": request.user.username,
            "types": [type_.name for type_ in feeder.types.all()]
        })


from rest_framework.pagination import PageNumberPagination
from catalog.serializers import PokemonSimpleSerializer

class AllMyPokemonsView(APIView, PageNumberPagination):

    permission_classes = [IsAuthenticated]
    page_size=20

    def get (self, request, format=None):

        print (f"Get all my pokemons")
        
        feeder = Feeder.objects.get(pk=request.user.id)
        categories = feeder.types.all()

        pokemons = Pokemon.objects.filter(types__in=categories)

        self.count = len(pokemons)

        results = self.paginate_queryset(pokemons, request, view=self)
        serializer = PokemonSimpleSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

        
class MyPokemonView(APIView):

    permission_classes = [IsAuthenticated]

    def get (self, request, pokemon_id_or_name, format=None):

        feeder = Feeder.objects.get(pk=request.user.id)
        categories = feeder.types.all()

        try:
            pokemon = (
                Pokemon.objects.get(pk=pokemon_id_or_name)
                if pokemon_id_or_name.isdigit()
                else Pokemon.objects.get(name=pokemon_id_or_name)
            )
        except Pokemon.DoesNotExist:
            msg_id_type = "id" if pokemon_id_or_name.isdigit() else "name"
            return Response(
                {
                    "message": f"Unkown pokemon for {msg_id_type} {pokemon_id_or_name}"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if not categories & pokemon.types.all():
            type_msg = ", ".join([type_.name for type_ in pokemon.types.all()])
            return Response(
                {
                    "message": f"Pokemon not in you collection because of type(s) - {type_msg} "
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(pokemon.description)