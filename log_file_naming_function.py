import os
import re
from datetime import datetime

def generate_unique_csv_filename():
    # Get current date components
    now = datetime.now()
    day = now.strftime("%d")
    month = now.strftime("%B")  # Full month name
    year = now.strftime("%Y")
    
    # File pattern for today's date
    date_str = f"{day}_{month}_{year}"
    pattern = re.compile(rf"test_(\d+)_({day}_{month}_{year})\.csv")

    max_test_number = 0

    # Scan current directory for matching files
    for filename in os.listdir('.'):
        match = pattern.match(filename)
        if match:
            test_number = int(match.group(1))
            if test_number > max_test_number:
                max_test_number = test_number

    # Next test number
    next_test_number = max_test_number + 1

    # Construct the filename
    filename = f"test_{next_test_number}_{date_str}.csv"
    return filename
