import requests
from datetime import datetime, timedelta
import time
import os


def get_tickets_all(api_baseurl, api_key):
    """
    Fetch all tickets from SyncroMSP API.

    Args:
    api_baseurl (str): SyncroMSP API base URL
    api_key (str): SyncroMSP API key

    Returns:
    list: List of all tickets
    """

    url = f'{api_baseurl}/tickets'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    all_syncro_tickets = []

    page = 1
    while True:
        response = requests.get(url, headers=headers, params={'page': page})
        if response.status_code == 200:
            tickets_data = response.json().get('tickets', [])
            all_syncro_tickets.extend(tickets_data)

            meta = response.json().get('meta', {})
            total_pages = meta.get('total_pages', 0)
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(1)
        else:
            raise Exception(f"Failed to fetch tickets from SyncroMSP API. Status code: {response.status_code}, Response: {response.text}")

    return all_syncro_tickets

def get_tickets_recently_updated(api_baseurl, api_key, days):
    """
    Fetch recently updated tickets from SyncroMSP API

    Args:
    api_baseurl (str): SyncroMSP API base URL
    api_key (str): SyncroMSP API key
    days (int): Number of days to look back for updated tickets

    Returns:
    list: List of filtered tickets
    """

    url = f'{api_baseurl}/tickets'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    query_days = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    params = {'since_updated_at': query_days}

    syncro_tickets = []

    page = 1
    while True:
        response = requests.get(url, headers=headers, params={**params, 'page': page})
        print(f"Response Headers for page {page}: {response.headers}")

        if response.status_code == 200:
            tickets_data = response.json().get('tickets', [])
            syncro_tickets.extend(tickets_data)

            meta = response.json().get('meta', {})
            total_pages = meta.get('total_pages', 0)
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(1)
        else:
            raise Exception(f"Failed to fetch tickets from SyncroMSP API. Status code: {response.status_code}, Response: {response.text}")

    return syncro_tickets


def get_tickets_customer_id(api_baseurl, api_key, customer_id):
    """
    Fetch all tickets for a specific customer ID
    """
    import requests
    import time
    
    url = f'{api_baseurl}/tickets'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    syncro_tickets_customer = []

    page = 1
    while True:
        response = requests.get(url, headers=headers, params={'customer_id': customer_id, 'page': page})
        if response.status_code == 200:
            tickets_data = response.json().get('tickets', [])
            syncro_tickets_customer.extend(tickets_data)

            meta = response.json().get('meta', {})
            total_pages = meta.get('total_pages', 0)
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(1)
        else:
            raise Exception(f"Failed to fetch tickets from SyncroMSP API. Status code: {response.status_code}, Response: {response.text}")

    return syncro_tickets_customer


def get_ticket(api_baseurl, api_key, ticket_id):
    """
    Fetch a ticket from SyncroMSP API

    Args:
    api_baseurl (str): SyncroMSP API base URL
    api_key (str): SyncroMSP API key
    ticket_id (int): Ticket ID

    Returns:
    dict: Ticket data
    """

    url = f'{api_baseurl}/tickets/{ticket_id}'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            raise Exception(f"Invalid JSON response from SyncroMSP API. Response: {response.text}")
        
        ticket_data = data.get('ticket')
        if ticket_data is None:
            raise Exception(f"Ticket data not found in SyncroMSP API response. Response: {response.text}")

        return ticket_data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch ticket from SyncroMSP API: {e}")
