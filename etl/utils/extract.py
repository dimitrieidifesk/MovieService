import datetime


class Extractor:
    def __init__(self, producer, state):
        self.producer = producer
        self.state = state

    def extract(self, table, batch):
        try:
            last_timestamp = self.state.get_state()
        except AttributeError:
            last_timestamp = "1000-01-16 00:00:00"  # Some old datetime
        self.producer.extract_movie(last_timestamp)
        data = self.producer.fetch_movies(batch=batch)
        if data:
            last_timestamp = data[-1][-1]
            self.state.set_state(
                (last_timestamp + datetime.timedelta(seconds=1)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        return data
