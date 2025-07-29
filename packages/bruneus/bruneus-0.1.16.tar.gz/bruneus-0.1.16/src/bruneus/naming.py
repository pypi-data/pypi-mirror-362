import random
import string
from datetime import datetime


def random_table_name(prefix):
    suffix = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}{current_datetime}-{suffix}"
