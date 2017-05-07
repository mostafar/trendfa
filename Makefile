
load-schema:
		docker-compose exec db mysql -ptoor trendfa < schema.sql

mysql:
		docker-compose exec db mysql trendfa

process-timeline:
		docker-compose run -d trendfa python3 -m trendfa.process_timeline

trends:
		docker-compose run trendfa python3 -m trendfa.tweet_trends

tweet-trends:
		docker-compose run trendfa python3 -m trendfa.tweet_trends --send

records:
		docker-compose run trendfa python3 -m trendfa.tweet_records

tweet-records:
		docker-compose run trendfa python3 -m trendfa.tweet_records --send
