import requests
from tqdm import tqdm

from django.core.management.base import BaseCommand

from catalog.models import Pokemon, Type


class Command(BaseCommand):

    types = {}

    def __all_types(self):
        """
        Get all types of pokemon
        """

        response = requests.get("https://pokeapi.co/api/v2/type")
        json = response.json()

        for result in json["results"]:
            # print(result["name"])
            type_, _  = Type.objects.get_or_create(name=result["name"])
            self.types[result["name"]] = type_


    def __all_pokemons(self):
        
        json_response = requests.get("https://pokeapi.co/api/v2/pokemon/").json()
        total_pokemons = json_response["count"]

        with tqdm(total=total_pokemons) as pbar:
            while json_response["results"]:

                for json_pokemon in json_response["results"]:
                    
                    description = requests.get(json_pokemon["url"]).json()

                    pok = {
                        "public_id":json_pokemon["url"].split("/")[-2],
                        "name":json_pokemon["name"],
                        "url":json_pokemon["url"],
                        "types": [type_entry["type"]["name"] for type_entry in description["types"]],
                        "description":description,
                    }

                    pokemon, _ = Pokemon.objects.get_or_create(
                        poke_id = json_pokemon["url"].split("/")[-2],
                        name = json_pokemon["name"],
                        url = json_pokemon["url"],
                        description = description,
                    )

                    for type_name in [type_entry["type"]["name"] for type_entry in description["types"]]:
                        pokemon.types.add(self.types[type_name])

                    pbar.update(1)

                if json_response["next"]:
                    json_response = requests.get(json_response["next"]).json()
                else:
                    break


    def handle(self, *args, **options):
    
        self.__all_types()
        print("Pokemon types loaded")
        self.__all_pokemons()

        print("Pokemons loaded")
        