
dump-schema:
		docker-compose exec db mysqldump --no-data -ptoor trendfa > schema.sql

load-schema:
		docker-compose exec db mysql -ptoor trendfa < schema.sql

process-timeline:
		docker-compose exec trendfa python3 process_timeline.py
