# United Nations Network Analysis

This project is an analysis of international relations through social network theory.

There are two main phases to the project.
- Gathering United Nations voting data with a web crawler.
- Creating IR graphs out of that data and analyzing them.

## Crawler

### crawl.py

This is the main script. It downloads all data from the UN voting database and saves it to separate CSV files for each year.

One row in the database is called a **record**.

When running the script you can give it a single year or a year range to crawl. By default it will access all years from 1946 to 2024.

### verify.py

This script checks files for years 1946 to 2024 to make sure the expected number of records is present, and that none of the records have any missing data.

The expected record counts are sourced from the *expected_record_count.txt* file.

The script will report any errors it encounters for manual patching.

### merge.py

This script merged all records from the per-year files (1946 to 2024) into one master file.

It works by using pandas which has a more strict CSV parsing system than Excel (specifically regarding quotations), which makes it work as an additional point of verification.