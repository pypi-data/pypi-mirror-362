from logging import Handler, LogRecord
from datetime import datetime, timezone, timedelta

class CosmosHandler(Handler):
    
    def __init__(self, collection, days_to_expiration: int) -> None:
        super().__init__()
        from pymongo.collection import Collection
        self.collection: Collection = collection
        self.days_to_expiration = days_to_expiration
        self.indexes = self.collection.index_information()

    def emit(self, record: LogRecord):

        document = self.format(record)

        if 'expireAt_1' not in self.indexes:             
            self.collection.create_index("expireAt", expireAfterSeconds=0)

        if self.days_to_expiration:
            utc_timestamp = datetime.now(timezone.utc)
            document["expireAt"] = utc_timestamp + timedelta(days=self.days_to_expiration)

        self.collection.insert_one(document)