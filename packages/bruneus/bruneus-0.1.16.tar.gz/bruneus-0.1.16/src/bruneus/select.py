from google.cloud import bigquery
from jinja2 import Template, Environment, FileSystemLoader
from .create_table import create_table
import google.cloud.bigquery


class SelectTask:
    def __init__(self, client, query):
        self.client = client
        self.query = query
        self.query_parameters = []

    def params(self, params):
        self.query_parameters = params
        return self

    def add_scalar_param(self, key: str, value: int, data_type: str):
        if self.query_parameters is None:
            self.query_parameters = []

        self.query_parameters.append(
            bigquery.ScalarQueryParameter(key, data_type, value),
        )
        return self

    def int64_param(self, key: str, value: int):
        return self.add_scalar_param(key, value, "INT64")

    def str_param(self, key: str, value: str):
        return self.add_scalar_param(key, value, "STRING")

    def float64_param(self, key: str, value: float):
        return self.add_scalar_param(key, value, "FLOAT64")

    def add_array_param(self, key: str, values: list, data_type: str):
        if self.query_parameters is None:
            self.query_parameters = []

        self.query_parameters.append(
            bigquery.ArrayQueryParameter(key, data_type, values),
        )
        return self

    def int64_array_param(self, key: str, values: list[int]):
        return self.add_array_param(key, values, "INT64")

    def str_array_param(self, key: str, values: list[str]):
        return self.add_array_param(key, values, "STRING")

    def float64_array_param(self, key: str, values: list[float]):
        return self.add_array_param(key, values, "FLOAT64")

    def bq_client(self):
        return self.client if self.client is not None else bigquery.Client()

    def job(self, dry_run=False, use_query_cache=True):
        job_config = bigquery.QueryJobConfig(query_parameters=self.query_parameters, dry_run=dry_run, use_query_cache=use_query_cache)
        return self.bq_client().query(self.query, job_config=job_config)

    def as_dicts(self):
        query_job = self.job()
        return [dict(row) for row in query_job]

    def stringify(
        self, names={}, delimiter="\n", format="{{ name }}({{ key }}): {{ value }}"
    ):
        dicts = self.as_dicts()
        strings = []
        for d in dicts:
            formatted_fields = []
            for k, v in d.items():
                name = names.get(k, k)
                formatted_str = Template(format).render(key=k, name=name, value=v)
                formatted_fields.append(formatted_str)
            strings.append(delimiter.join(formatted_fields))
        return strings

    def first_as_dict(self):
        dicts = self.as_dicts()
        if len(dicts) == 0:
            return None
        return self.as_dicts()[0]

    def to_table(self, table_id, overwrite=False):
        return create_table(
            table_id,
            self.query,
            self.query_parameters,
            overwrite=overwrite,
            client=self.client,
        )

    def to_dataframe(self):
        return self.job().to_dataframe()

    def to_df(self):
        return self.to_dataframe()

    def dry_run(self, use_query_cache=False):
        return self.job(dry_run=True, use_query_cache=use_query_cache)


def select(
    query: str,
    query_parameters=None,
    client: google.cloud.bigquery.Client = None,
):
    return SelectTask(client=client, query=query).params(
        [] if query_parameters is None else query_parameters
    )


def select_with_template(
    template_dir: str, template_name: str, template_parameters={}, client=None
):
    env = Environment(loader=FileSystemLoader(template_dir, encoding="utf8"))
    tmpl = env.get_template(template_name)
    query = tmpl.render(template_parameters)

    return select(query=query, query_parameters=[], client=client)
