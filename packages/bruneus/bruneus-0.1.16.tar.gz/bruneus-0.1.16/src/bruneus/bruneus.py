from .select import select


class Bruneus:
    def __init__(self, bq_client):
        self.bq_client = bq_client

    def select(self, query, query_parameters):
        return select(
            client=self.bq_client, query=query, query_parameters=query_parameters
        )
