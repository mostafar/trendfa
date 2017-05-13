## Running Example

https://twitter.com/Trendfa

## Synopsis

TrendFa processes Twitter timeline to find top trending Persian words. It uses [hazm](https://github.com/sobhe/hazm) as Persian sentence tokenizer.

## Installation

Build docker containers and load database schema by:

```
docker-compose build
make load-schema
```

Add Twitter API credentials into `trendfa/twitter.py` and test your installation by running:

```
make process-timeline
```

It will run in background and might take about 30 minutes because of Twitter API rate-limit (You can check the process using `docker ps`), when finished try:

```
make trends
```

to see top trends loading from database.

## Contributors

You're more than welcome to improve TrendFa, feel free to submit a pull request :)

