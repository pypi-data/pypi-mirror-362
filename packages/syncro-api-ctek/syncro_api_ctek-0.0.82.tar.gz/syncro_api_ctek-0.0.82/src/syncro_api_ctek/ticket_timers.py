import requests
import time
import os


def get_ticket_timers(api_baseurl, api_key, created_at_gt=None):
    """
    Retrieve a list of ticket timers from the API with pagination and optional filtering.
    
    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.
        created_at_gt (str, optional): A filter for retrieving ticket timers created after this date/time. Format: YYYY-MM-DD
    
    Returns:
        list: A list of ticket_timers.
    """
    url = f'{api_baseurl}/ticket_timers'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    all_syncro_ticket_timers = []

    page = 1
    while True:
        params = {'page': page}
        if created_at_gt:
            params['created_at_gt'] = created_at_gt

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            ticket_timers_data = response.json().get('ticket_timers', [])
            all_syncro_ticket_timers.extend(ticket_timers_data)

            meta = response.json().get('meta', {})
            total_pages = meta.get('total_pages', 0)
            if page >= total_pages:
                break
            else:
                page += 1
                time.sleep(1)
        else:
            raise Exception(f"Failed to fetch ticket timers from SyncroMSP API. Status code: {response.status_code}, Response: {response.text}")

    return all_syncro_ticket_timers
