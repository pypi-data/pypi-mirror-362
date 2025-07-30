import requests
import logging
import time
import os

logger = logging.getLogger(__name__)

def get_contacts_by_customer(api_baseurl, api_key, customer_id):
    """
    Retrieve contacts for a specific customer from the API.
    
    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.
        customer_id (str): The ID of the customer to retrieve contacts for.
    
    Returns:
        list: A list of contacts for the specified customer.
    
    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """
    if not api_baseurl:
        raise ValueError("API base URL must be provided.")
    if not api_key:
        raise ValueError("API key must be provided.")
    if not customer_id:
        raise ValueError("Customer ID must be provided.")
    
    url = f'{api_baseurl}/contacts'
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    contacts = []
    page = 1
    
    while True:
        params = {"customer_id": customer_id, "page": page}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()

            if "contacts" not in data or "meta" not in data or "total_pages" not in data["meta"]:
                logger.error(f"Unexpected response structure: {data}")
                break
            
            contacts.extend(data["contacts"])
            
            if page >= data["meta"]["total_pages"]:
                break
            page += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            raise

    return contacts

def get_contacts_all_customers(api_baseurl, api_key):
    """
    Retrieve all contacts from the API across all customers.
    
    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.
    
    Returns:
        list: A list of all contacts.
    
    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """
    if not api_baseurl:
        raise ValueError("API base URL must be provided.")
    
    if not api_key:
        raise ValueError("API key must be provided.")
    
    url = f'{api_baseurl}/contacts'
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    contacts = []
    page = 1
    
    while True:
        params = {"page": page}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Validate the response structure
            if "contacts" not in data or "meta" not in data or "total_pages" not in data["meta"]:
                logger.error(f"Unexpected response structure: {data}")
                break
            
            contacts.extend(data["contacts"])
            
            if page >= data["meta"]["total_pages"]:
                break
            page += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            raise  # Re-raise the exception so the caller can handle it

    return contacts

