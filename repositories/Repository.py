from typing import Generic, TypeVar
import os
from azure.cosmos import CosmosClient, exceptions
from abc import ABC, abstractmethod
from collections import Counter
from models.BaseModel import BaseModel

T = TypeVar("T", bound=BaseModel)

class Repository(ABC, Generic[T]):
    ENV_KEY_ACCOUNT_URI = "COSMOS_ACCOUNT_URI"
    ENV_KEY_ACCOUNT_KEY = "COSMOS_ACCOUNT_KEY"
    ENV_KEY_DATABASE_KEY = "COSMOS_DATABASE"

    def __init__(self, container_name: str) -> None:
        url = os.environ[self.ENV_KEY_ACCOUNT_URI]
        key = os.environ[self.ENV_KEY_ACCOUNT_KEY]
        db_name = os.environ[self.ENV_KEY_DATABASE_KEY]
        client = CosmosClient(url, credential=key)
        database = client.get_database_client(db_name)
        container = database.get_container_client(container_name)
        self.container = container
    
    
    def create(self, model: T):
        self.container.create_item(
            self.dump_item(model)
        )
    
    def retrieve_all(self) -> T:
        results = None
        results = list(self.container.query_items(query="SELECT * FROM r",
            enable_cross_partition_query=True
        ))

        if (results is None or not results):
            return []
        else:
            try:
                return [self.parse_item(item) for item in results]
            except exceptions.CosmosResourceNotFoundError:
                return None

    def retrieve(self, id: str) -> T:    
        query, parameters, perform_query = self.query_maker(id)
        if perform_query:
            results = list(self.container.query_items(query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
        else:
            results = None
        if (results is None or not results):
            return None
        else:
            try:
                return self.parse_item(results[0])
            except exceptions.CosmosResourceNotFoundError:
                return None
            
    def update(self, model: T) -> T:
        self.container.upsert_item(
            self.dump_item(model)
        )
        return model
    
    def delete(self, partition_key: str, id: str) -> None:
        self.container.delete_item(
            id,
            partition_key=partition_key
        )
    
    @abstractmethod
    def parse_item(self, item: dict) -> T:
        pass

    @abstractmethod
    def dump_item(self, item: T) -> dict:
        pass

    def count_items(self) -> int:
        results = list(self.container.query_items(query="SELECT VALUE COUNT(1) FROM r",
            enable_cross_partition_query=True
        ))
        return results[0]
    
    def count_generated_songs(self) -> int:
        results = list(self.container.query_items(query="SELECT VALUE COUNT(1) FROM r WHERE r.song_created=true",
            enable_cross_partition_query=True
        ))
        return results[0]
    
    def count_sent_sms(self) -> int:
        results = list(self.container.query_items(query="SELECT VALUE COUNT(1) FROM r WHERE r.sms_sent=true",
            enable_cross_partition_query=True
        ))
        return results[0]

    def calculate_language_breakdown(self) -> dict:
        # Get all languages
        query = "SELECT r.language FROM r"
        results = list(self.container.query_items(query=query, enable_cross_partition_query=True))

        # Count the occurrences of each language
        languages = [item['language'] for item in results if item['language'] is not None]
        counts = Counter(languages)

        return dict(counts)
    
    def count_repeat_phone_numbers(self) -> int:
        # Get all phone numbers
        query = "SELECT r.phone_number FROM r"
        results = list(self.container.query_items(query=query, enable_cross_partition_query=True))

        # Count the occurrences of each phone number
        phone_numbers = [item['phone_number'] for item in results]
        counts = Counter(phone_numbers)

        # Count the number of phone numbers that appear more than once
        repeat_phone_numbers = sum(1 for count in counts.values() if count > 1)

        return repeat_phone_numbers

    def query_maker(self, id):
        perform_query = True

        query = "SELECT * FROM r WHERE r.id=@id "
        parameters = [{"name":"@id", "value": id}]

        return query, parameters, perform_query
    
    def query_maker_by_user_id(self, user_id):
        perform_query = True

        query = "SELECT * FROM r WHERE r.user_id=@user_id "
        parameters = [{"name":"@user_id", "value": user_id}]

        return query, parameters, perform_query    