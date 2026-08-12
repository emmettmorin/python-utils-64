import time
import requests

class NetworkError(Exception):
    pass

def retry_request(url, retries=3, delay=2):
    attempts = 0
    while attempts < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()  # Assuming we want JSON data
        except requests.RequestException:
            attempts += 1
            if attempts >= retries:
                raise NetworkError(f'Failed to fetch data from {url} after {retries} attempts')
            time.sleep(delay)
    return None

# Example usage:
# data = retry_request('https://api.example.com/data')
# print(data)  # Handle your data here