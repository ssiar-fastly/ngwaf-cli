# NG WAF Sites List Script

This Python script retrieves a list of sites from the Fastly NG WAF API, handling pagination to ensure all sites are retrieved. It also outputs the site names and display names into a CSV file.

## Prerequisites

- Python 3.x
- `requests` library

You can install the `requests` library using pip:

```sh
pip install requests
```

## Usage

### Command-Line Arguments

- `--ngwaf_user_email` (required): NGWAF user email.
- `--ngwaf_token` (required): NGWAF API token.
- `--corp_name` (required): Corporation name.
- `--csv_file` (required): Path to output CSV file.

### Running the Script

1. Save the script as `list_sites.py`.
2. Run the script from the command line, providing the required arguments. For example:

```sh
python list_sites.py --ngwaf_user_email="your_email" --ngwaf_token="your_api_token" --corp_name="your_corp_name" --csv_file="output_sites.csv"
```

### Example

```sh
python list_sites.py --ngwaf_user_email="example@example.com" --ngwaf_token="your_api_token" --corp_name="example_corp" --csv_file="sites.csv"
```

### Environment Variables

Alternatively, you can set the required arguments as environment variables:

- `NGWAF_USER_EMAIL`: NGWAF user email.
- `NGWAF_TOKEN`: NGWAF API token.
- `CORP_NAME`: Corporation name.
- `CSV_FILE`: Path to output CSV file.

Then you can run the script without providing those arguments:

```sh
python list_sites.py
```

### Script Output

The script will print the total number of sites retrieved and their names and display names. It will also write the site names and display names to the specified CSV file, including a header row.

### Error Handling

The script includes retry logic for API calls. If an API call fails, it will retry up to three times, with a 10-second wait between retries. If an API call fails with an unauthorized (401) error, no retry will be attempted.

## Contact

Sina Siar - [@ssiar](https://linkedin.com/in/ssiar) - ssiar@fastly.com
