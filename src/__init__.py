import logging
from datetime import datetime
import os

logdir = "logs"
os.makedirs(logdir, exist_ok=True)

now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute
second = now.second

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    filename=os.path.join(
        logdir, f"app.log" # -{year}-{month}-{day}-{hour}-{minute}-{second}
    ),
    filemode="w",
    encoding="utf-8",
)
