# PokeAPi
- Django
- DRF
- CELERY
- REDIS
#### RUN REDIS DOCKER
`docker run -d -p 6379:6379 redis`
<p>Run docker instance to use such as a broker and results backend</p>

#### RUN CELERY WORKER
`celery -A pokemonApi worker --loglevel=INFO`

### COMMANDS
* get_evolution_chain
<br>`python manage.py get_evolution_chain --id CHAIN_ID`
<br> Create full evolution chain from pokeapi to DB by id
<br>This command execute a celery tasks and other celery chain tasks to enqueue db transactions to perform process
<br>(Get id from original pokeapi `https://pokeapi.co/api/v2/evolution-chain/{id}/)`

### ENDPOINTS
* Docs url - `http://localhost:8000/swagger/`
* Get pokemon from id (Id stored in django DB)
`http://localhost:8000/pokemon/{id}/`

```
HTTP GET - JSON RESPONSE

{
  "name": "pikachu",
  "weight": "60.0",
  "height": "4.0",
  "external_id": "25",
  "specie": "pikachu - 25",
  "stats": [
    {
      "base_stat": 50,
      "effort": 0,
      "name": "special-attack"
    },
    {
      "base_stat": 35,
      "effort": 0,
      "name": "hp"
    },
    {
      "base_stat": 55,
      "effort": 0,
      "name": "attack"
    },
    {
      "base_stat": 40,
      "effort": 0,
      "name": "defense"
    },
    {
      "base_stat": 50,
      "effort": 0,
      "name": "special-defense"
    },
    {
      "base_stat": 90,
      "effort": 2,
      "name": "speed"
    }
  ],
  "evolution_chain": {
    "external_id": 10,
    "specie": "pichu - 172",
    "evolutions": [
      {
        "evolution_type": "",
        "external_id": 5,
        "name": "raichu",
        "specie": "raichu - 26"
      },
      {
        "evolution_type": "",
        "external_id": 4,
        "name": "pikachu",
        "specie": "pikachu - 25"
      }
    ]
  }
}
```