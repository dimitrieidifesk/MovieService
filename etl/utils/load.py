class Loader:
    def __init__(self, consumer):
        self.consumer = consumer
        self.consumer.create_index()

    def load_data(self, body):
        self.consumer.insert_request(body=body)
