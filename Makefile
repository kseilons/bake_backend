# Makefile for managing Docker operations and database backups

# Command to create a backup
backup:
	docker exec -t bake_db_container pg_dump -U bake_user bake_db > backup

# Command to load a backup
load_backup:
	docker cp backup bake_db_container:/backup
	docker exec -i bake_db_container psql -U bake_user -d bake_db < backup

# Command to start Docker containers using docker-compose
start:
	docker-compose up
