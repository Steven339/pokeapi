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
* get_evolution_chain<br>(Get id from original pokeapi <br>`https://pokeapi.co/api/v2/evolution-chain/{id}/)`
<br>`python manage.py get_evolution_chain --id CHAIN_ID`
<br> This command execute a celery tasks and other celery chain tasks to enqueue db transactions to perform process

### ENDPOINTS
* Get pokemon from id (Id stored in django DB)
`http://localhost:8000/pokemon/{id}/`