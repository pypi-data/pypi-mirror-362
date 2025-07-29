from google.cloud import bigquery
from google.cloud.bigquery import Table


class CSVExport:
    def __init__(self, task, field_delimiter, gzip, print_header):
        self.task = task
        self.field_delimiter = field_delimiter
        self.gzip = gzip
        self.print_header = print_header

    def to_gcs(self, bucket, object_name):
        destination_uri = f"gs://{bucket}/{object_name}"

        c = self.task.get_bq_client()

        job_config = bigquery.job.ExtractJobConfig()
        if self.gzip:
            job_config.compression = bigquery.Compression.GZIP
        job_config.field_delimiter = self.field_delimiter
        job_config.print_header = self.print_header

        extract_job = c.extract_table(
            Table.from_string(self.task.table_id),
            destination_uri,
            location=self.task.location,
            job_config=job_config,
        )

        extract_job.result()

        return destination_uri


class ExportTask:
    def __init__(self, table_id, location=None, project=None, client=None):
        self.table_id = table_id
        self.location = location
        self.project = project
        self.bq_client = client

    def get_bq_client(self):
        if self.bq_client is not None:
            return self.bq_client
        return bigquery.Client(project=self.project)

    def as_csv(self, field_delimiter=",", gzip=False, print_header=True):
        return CSVExport(
            task=self,
            field_delimiter=field_delimiter,
            gzip=gzip,
            print_header=print_header,
        )


def export_table(table_id, location=None, project=None, client=None):
    return ExportTask(
        table_id=table_id, location=location, project=project, client=client
    )
