
load-schema:
		docker-compose exec db mysql -ptoor trendfa < schema.sql

mysql:
		docker-compose exec db mysql trendfa

process-timeline:
		docker-compose run -d trendfa python3 process_timeline.py

trends:
		docker-compose run trendfa python3 tweet_trends.py

tweet-trends:
		docker-compose run trendfa python3 tweet_trends.py --send

records:
		docker-compose run trendfa python3 tweet_records.py

tweet-records:
		docker-compose run trendfa python3 tweet_records.py --send
