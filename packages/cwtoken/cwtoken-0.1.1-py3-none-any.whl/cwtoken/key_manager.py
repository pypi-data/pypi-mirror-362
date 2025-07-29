import requests
import pandas as pd

base_url = 'https://atukpostgrest.clubwise.com/'

def get_access_token(clubcode: str, api_token: str, timeout: int = 10, verbose: bool = False) -> str:
    """
    Fetch access-token from the API.

    Args:
        clubcode (str): The club's unique identifier.
        api_token (str): The authentication token or secret.
        timeout (int): Timeout duration in seconds.
        verbose (bool): If True, print detailed error messages.

    Returns:
        str or None: Access token if successful, otherwise None.
    """
    request_url = base_url + 'access-token'
    request_header = {
        'CW-API-Token': api_token,
        'Content-Type': 'application/json'
    }
    request_payload = {'sClubCode': clubcode}

    try:
        response = requests.post(request_url, json=request_payload, headers=request_header, timeout=timeout)
        response.raise_for_status()
        my_token = response.json().get('access-token')

        if not my_token:
            print("Access token not found in response. Check your club code and API token.")
            return None

        return my_token

    except requests.exceptions.RequestException as e:
        print("Error generating access token.")
        if verbose:
            print(f"Details: {e}")
        return None

def fetch(clubcode: str, api_token: str, request: str, timeout: int = 10, verbose: bool = False) -> pd.DataFrame:
    """
    Fetch data from the API.

    Args:
        clubcode (str): The club's unique identifier.
        api_token (str): The authentication token or secret.
        request (str): The endpoint or request type (e.g., 'players').
        timeout (int): Timeout duration in seconds.
        verbose (bool): If True, print detailed error messages.

    Returns:
        pd.DataFrame or None: Data as a DataFrame if successful, otherwise None.
    """
    my_token = get_access_token(clubcode, api_token, timeout=timeout, verbose=verbose)
    if not my_token:
        print("\nFailed to fetch access token. Aborting.")
        print("Try running test_connection() or check your club code and static token.\n")
        return None

    access_headers = {
        'CW-API-Token': api_token,
        'Authorization': f'Bearer {my_token}'
    }
    combined_url = base_url + request

    try:
        response = requests.get(combined_url, headers=access_headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)

    except requests.exceptions.RequestException as e:
        print("Error fetching data from API.")
        if verbose:
            print(f"Details: {e}")
        return None
