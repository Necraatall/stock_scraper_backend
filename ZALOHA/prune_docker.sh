#!/bin/bash

# Zastavení všech běžících kontejnerů
docker stop $(docker ps -aq)

# Odstranění všech kontejnerů
docker rm $(docker ps -aq)

# Odstranění všech obrazů
docker rmi $(docker images -q)

# Odstranění všech svazků
docker volume rm $(docker volume ls -q)

# Odstranění všech sítí
docker network rm $(docker network ls -q)

# Kompletní vyčištění systému
docker system prune -a --volumes -f
