# bruneus
[![Maintainability](https://api.codeclimate.com/v1/badges/c9d020ea15b032c4cefb/maintainability)](https://codeclimate.com/github/yokoe/bruneus/maintainability)

BigQuery helper library for Python

## How to use
### Select from table
```
import bruneus
bruneus.select("SELECT * FROM `foo.bar.purchases` LIMIT 20").as_dicts()
bruneus.select("SELECT * FROM `foo.bar.purchases` ORDER BY created_at LIMIT 1", client=bigquery.Client(project="foobar")).first_as_dict()
bruneus.select("SELECT * FROM `foo.bar.purchases` LIMIT 20").to_dataframe()

bruneus.select("SELECT word, word_count FROM `bigquery-public-data.samples.shakespeare` LIMIT 5").stringify(names={"word": "Word", "word_count": "Word count"})
```

### Create table from query
```
bruneus.select("SELECT * FROM `some.source.table`").to_table("foo.bar.new_table")
```

### Create temp table from query
```
bruneus.select("SELECT * FROM `some.source.table`").to_table("foo.bar.new_table").expires_in(days=7)
```

### Export table to GCS as csv
```
bruneus.export_table("foo.bar.sample").as_csv(gzip=True).to_gcs("my-bucket", "exported-table.csv.gz")
```


### Generate random table name
```
bruneus.random_table_name("prefix-here")
```

## Development
### Run tests
```
docker compose run bruneus
```
