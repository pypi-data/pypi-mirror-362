import requests
import time
import os

def get_assets_all(api_baseurl, api_key):
    """
    Retrieve assets from the API across all customers.

    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of all assets.

    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """

    url = f'{api_baseurl}/customer_assets'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    all_assets = []
    page = 1

    while True:
        params = {"page": page}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_assets.extend(data["assets"])
            meta = data.get('meta', {})
            total_pages = meta.get('total_pages', 1)
            
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(1)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch assets on page {page}: {str(e)}")
        
    return all_assets

def get_assets_by_type(api_baseurl, api_key, asset_type_id):
    """
    Retrieve assets from the API across all customers, for a specific asset type.

    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of all assets of the requested type.

    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """

    url = f'{api_baseurl}/customer_assets'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    all_assets = []
    page = 1

    while True:
        params = {
            "page": page,
            "asset_type_id": asset_type_id
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Add assets to the list
            all_assets.extend(data["assets"])
            
            # Pagination handling
            meta = data.get('meta', {})
            total_pages = meta.get('total_pages', 1)
            
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(1)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch assets on page {page}: {str(e)}")
        
    return all_assets
