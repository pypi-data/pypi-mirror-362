from google.cloud import bigquery
from datetime import timedelta, datetime, timezone
from google.cloud.bigquery import Table
from .export_table import ExportTask


class CreateTableResult:
    def __init__(self, client, table_id):
        self.client = client
        self.table_id = table_id

    def expires_in(self, days):
        table = self.client.get_table(Table.from_string(self.table_id))
        expiration = datetime.now(timezone.utc) + timedelta(days=days)
        table.expires = expiration
        table = self.client.update_table(table, ["expires"])
        return self

    def export(self):
        return ExportTask(table_id=self.table_id)


def create_table(
    table_id, query, query_parameters=[], overwrite=False, project=None, client=None
):
    c = client
    if c is None:
        c = bigquery.Client(project=project)

    write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
    if overwrite:
        write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config = bigquery.QueryJobConfig(
        destination=table_id,
        write_disposition=write_disposition,
        query_parameters=query_parameters,
    )
    query_job = c.query(query, job_config=job_config)
    query_job.result()

    return CreateTableResult(c, table_id)
