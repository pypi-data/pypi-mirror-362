import unittest
import bruneus
from dotenv import load_dotenv

load_dotenv()


class TestSelect(unittest.TestCase):
    def test_select_with_no_params(self):
        query = "SELECT 1"
        task = bruneus.select(query)
        self.assertEqual(query, task.query)

    def test_select(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare` order by rand() limit 5"
        words = bruneus.select(query).as_dicts()
        self.assertEqual(len(words), 5)

    def test_select_with_no_result(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare` where word = 'abcdef-012345' order by rand() limit 5"
        word = bruneus.select(query).first_as_dict()
        self.assertIsNone(word)

    def test_select_with_template(self):
        words = (
            bruneus.select_with_template("./tests/templates", "shakespeare.j2")
            .int64_param("max_count", 3)
            .as_dicts()
        )
        self.assertEqual(len(words), 3)

    def test_select_to_dataframe(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare` order by rand() limit 5"
        df = bruneus.select(query).to_dataframe()
        self.assertEqual(len(df.index), 5)

    def test_select_to_stringified_array(self):
        query = """
        SELECT
        word, word_count
        FROM `bigquery-public-data.samples.shakespeare` 
        WHERE 
        LENGTH(word) >= 5 AND word_count >= 30
        ORDER BY word LIMIT 5
        """
        strings = bruneus.select(query).stringify(
            names={
                "word": "Word",
                "word_count": "Word Count",
            },
            delimiter="\n",
            format="{{ name }}({{ key }}): {{ value }}",
        )
        self.assertEqual(len(strings), 5)

        for s in strings:
            self.assertIn("Word(", s)
            self.assertIn("Word Count(", s)

    def test_select_to_stringified_array_on_empty_data(self):
        query = """
        SELECT
        word, word_count
        FROM `bigquery-public-data.samples.shakespeare` 
        WHERE 
        LENGTH(word) >= 99999
        ORDER BY word LIMIT 5
        """
        strings = bruneus.select(query).stringify(
            names={
                "word": "Word",
                "word_count": "Word Count",
            },
            delimiter="\n",
            format="{{ name }}({{ key }}): {{ value }}",
        )
        self.assertEqual(len(strings), 0)

    def test_select_int64_param(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare` order by rand() limit @max_count"
        select_task = bruneus.select(query)
        self.assertEqual(len(select_task.query_parameters), 0)
        select_task.int64_param("max_count", 5)
        self.assertEqual(len(select_task.query_parameters), 1)

    def test_select_int64_array_param(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare` WHERE word_count in UNNEST(@word_counts) order by rand() LIMIT 5"
        select_task = bruneus.select(query)
        self.assertEqual(len(select_task.query_parameters), 0)
        select_task.int64_array_param("word_counts", [10, 20, 30])
        self.assertEqual(len(select_task.query_parameters), 1)

    def test_select_str_array_param(self):
        query = "SELECT DISTINCT word FROM `bigquery-public-data.samples.shakespeare` WHERE word in UNNEST(@words)"
        select_task = bruneus.select(query)
        self.assertEqual(len(select_task.query_parameters), 0)
        select_task.str_array_param("words", ["quality", "that", "your"])
        self.assertEqual(len(select_task.query_parameters), 1)
        self.assertEqual(len(select_task.to_dataframe().index), 3)

    def test_select_float64_param(self):
        query = "SELECT count(1) FROM `bigquery-public-data.samples.gsod` WHERE mean_temp > @mean_temp"
        select_task = bruneus.select(query)
        self.assertEqual(len(select_task.query_parameters), 0)
        select_task.float64_param("mean_temp", 50.0)
        self.assertEqual(len(select_task.query_parameters), 1)
        self.assertEqual(len(select_task.to_dataframe().index), 1)

    def test_select_params(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare` order by rand() limit @max_count"
        task1 = bruneus.select(query).int64_param("max_count", 1)
        self.assertEqual(len(task1.query_parameters), 1)

        task2 = bruneus.select(query).int64_param("max_count", 2)
        self.assertEqual(len(task2.query_parameters), 1)

    def test_select_dry_run(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare`"
        result = bruneus.select(query).dry_run()
        self.assertTrue(result.total_bytes_processed > 0)

if __name__ == "__main__":
    unittest.main()
