import requests

types = []
count = 0

def all_types():
    """
    Get all types of pokemon
    """

    response = requests.get("https://pokeapi.co/api/v2/type")
    json = response.json()

    for result in json["results"]:
        types.append(result["name"])

    print ("Types are:", types)


def all_pokemons():

    global count
    
    json_response = requests.get("https://pokeapi.co/api/v2/pokemon/").json()
    
    while json_response["results"]:

        for pokemon in json_response["results"]:
            
            description = requests.get(pokemon["url"]).json()

            pok = {
                "poke_id":pokemon["url"].split("/")[-2],
                "name":pokemon["name"],
                "url":pokemon["url"],
                "types": [type_entry["type"]["name"] for type_entry in description["types"]],
                "description":description,
            }

            count += 1
            yield pok

            # for type in [type_entry["type"]["name"] for type_entry in description["types"]]:
            #     pokemon.types.add(types[type])

        if json_response["next"]:
            json_response = requests.get(json_response["next"]).json()
        else:
            break


if __name__ == "__main__":

    all_types()
    for pokemon in all_pokemons():
        print(pokemon["poke_id"], pokemon["name"], pokemon["types"])
    print (f"{count} pokemons")