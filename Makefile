
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

hashtags:
		docker-compose run trendfa python3 -m trendfa.tweet_hashtags

tweet-hashtags:
		docker-compose run trendfa python3 -m trendfa.tweet_hashtags --send

records:
		docker-compose run trendfa python3 -m trendfa.tweet_records

tweet-likes:
		docker-compose run trendfa python3 -m trendfa.tweet_records --send-likes

tweet-retweets:
		docker-compose run trendfa python3 -m trendfa.tweet_records --send-retweets
