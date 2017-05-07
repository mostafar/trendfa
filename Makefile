
dump-schema:
		docker-compose exec db mysqldump --no-data -ptoor --databases trendfa > schema.sql

load-schema:
		docker-compose exec db mysql -ptoor trendfa < schema.sql

process-timeline:
		docker-compose run -d trendfa python3 process_timeline.py

mysql:
		docker-compose exec db mysql trendfa

trends:
		docker-compose run trendfa python3 tweet_trends.py

tweet-trends:
		docker-compose run trendfa python3 tweet_trends.py --send

records:
		docker-compose run trendfa python3 tweet_records.py

tweet-records:
		docker-compose run trendfa python3 tweet_records.py --send
