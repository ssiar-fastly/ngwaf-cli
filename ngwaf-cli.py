import os
import requests
import argparse
import time
import csv

# Constants
BASE_URL = "https://dashboard.signalsciences.net/api/v0"
MAX_RETRIES = 3
RETRY_WAIT = 10

def get_headers(ngwaf_user_email, ngwaf_token):
    return {
        "Content-Type": "application/json",
        "x-api-user": ngwaf_user_email,
        "x-api-token": ngwaf_token
    }

def retry_api_call(func):
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < MAX_RETRIES:
            response = func(*args, **kwargs)
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                print("API call failed with Unauthorized (401) error. No retry will be attempted.")
                return response
            retries += 1
            error_message = response.text if response.text else "No additional error message provided"
            print(f"API call failed, response code: {response.status_code}. Error details: {error_message}. Retrying in {RETRY_WAIT}s... (Retry {retries}/{MAX_RETRIES})")
            time.sleep(RETRY_WAIT)
        return response
    return wrapper

@retry_api_call
def get_sites(ngwaf_user_email, ngwaf_token, corp_name, page, limit):
    url = f"{BASE_URL}/corps/{corp_name}/sites"
    params = {
        "page": page,
        "limit": limit
    }
    response = requests.get(url, headers=get_headers(ngwaf_user_email, ngwaf_token), params=params)
    return response

def get_all_sites(ngwaf_user_email, ngwaf_token, corp_name):
    all_sites = []
    page = 1
    limit = 10  # Adjust this value as needed
    
    while True:
        response = get_sites(ngwaf_user_email, ngwaf_token, corp_name, page, limit)
        if response.status_code != 200:
            print(f"Failed to retrieve sites: Status Code {response.status_code} - Details: {response.text}")
            break
        
        data = response.json().get('data', [])
        if not data:
            break
        
        all_sites.extend(data)
        page += 1
        
        if len(data) < limit:
            break  # Exit if there are fewer sites than the limit, indicating the last page
    
    return all_sites

def write_sites_to_csv(sites, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Site Name", "Display Name"])  # Write header row
        for site in sites:
            writer.writerow([site['name'], site['displayName']])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List NG WAF Sites")
    parser.add_argument('--ngwaf_user_email', default=os.environ.get('NGWAF_USER_EMAIL'), help='NGWAF user email', required=True)
    parser.add_argument('--ngwaf_token', default=os.environ.get('NGWAF_TOKEN'), help='NGWAF API token', required=True)
    parser.add_argument('--corp_name', default=os.environ.get('CORP_NAME'), help='Corporation name', required=True)
    parser.add_argument('--csv_file', default='sites.csv', help='Path to output CSV file', required=True)
    
    args = parser.parse_args()
    
    sites = get_all_sites(args.ngwaf_user_email, args.ngwaf_token, args.corp_name)
    
    if sites:
        print(f"Total sites retrieved: {len(sites)}")
        for site in sites:
            print(f"Name: {site['name']}, Display Name: {site['displayName']}")
        write_sites_to_csv(sites, args.csv_file)
        print(f"Site names written to {args.csv_file}")
    else:
        print("No sites found.")
