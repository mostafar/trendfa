from datetime import datetime, timedelta

from sqlalchemy import desc
from sqlalchemy import func

from database import session
from models import Word
from twitter import api as twitter_api


def get_trends(self, time_range, limit=5):
    session.query(Word)\
        .filter(Word.time >= (datetime.now() - time_range))\
        .group_by(Word.word)\
        .order_by(desc(func.count(Word.id)))\
        .limit(limit).all()


if __name__ == '__main__':
    # twitter_api.update_status()

    print(get_trends(timedelta(days=2)))
t