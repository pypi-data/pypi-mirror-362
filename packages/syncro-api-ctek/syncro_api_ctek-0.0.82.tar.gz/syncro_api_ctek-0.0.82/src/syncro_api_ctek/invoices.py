import requests
import time
import os


def get_invoices_all(api_baseurl, api_key):
    """
    Retrieve all invoices from API.

    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of all invoices.

    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """

    url = f'{api_baseurl}/invoices'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    all_invoices = []
    page = 1

    while True:
        params = {"page": page}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_invoices.extend(data["invoices"])
            meta = data.get('meta', {})
            total_pages = meta.get('total_pages', 1)
            
            if page >= total_pages:
                break
            else:
                page += 1
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch invoices on page {page}: {str(e)}")
        
    return all_invoices
