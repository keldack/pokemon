# IZBERG Back Dev Technical test
# SecurePokeAPI

## Goal

The purpose is to create a Python API over the public PokeAPI (https://pokeapi.co), in order to provide some authentication, because you need to earn your Pokemons!

## Instructions

### Step 1 - Access management API 

First, you need to create an access management API, with 4 routes:
- A route POST /api/login/, that logs the user in and returns a token.
- A route POST /api/group/<type>/add/, that adds the current user to the <type> group. The available types must match the Pokemon types in the PokeAPI (https://pokeapi.co/api/v2/type).
- A route POST /api/group/<type>/remove/, that removes the current user to the <type> group.
- A route GET /api/user/me/, returning the current user and groups he belongs to.


### Step 2 - Get them all!

Now that you have an access management API, you need to make a separate API that will consume it to grant access to the PokeAPI. Be aware that some pokemons have multiple types, you must handle this case properly.

- A route GET /api/pokemon/, returning a list of the Pokemons you have access to, depending on their types. You should have access to all the pokemons belonging in the groups you belong to, in the access management API.
- A route GET /api/pokemon/<id or name>/, returning the requested Pokemon details. Like the previous API call, the user must only  be able to access pokemons with a matching type.

