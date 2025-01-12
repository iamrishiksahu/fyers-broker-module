import requests
from .Logger import Logger

class APIUtil:
    
    @staticmethod
    def _handle_response(response):
        """Helper function to handle and check API responses."""
        return response
    @staticmethod
    def get(api_url, session=requests, headers={}, params=None):
        """Send a GET request."""
        url = f"{api_url}"
        Logger.log("GET:", url)
        try:
            response = session.get(url, params=params, headers=headers)
            return APIUtil._handle_response(response)
        except requests.exceptions.RequestException as e:
            Logger.log(f"GET request to {url} failed: {e}")
            return None

    @staticmethod
    def post(api_url, session=requests, headers={}, data=None, json_data=None):
        """Send a POST request."""
        url = f"{api_url}"
        Logger.log("POST:", url)
        
        try:
            response = session.post(url, data=data, json=json_data, headers=headers)
            return APIUtil._handle_response(response)
        except requests.exceptions.RequestException as e:
            Logger.log(f"POST request to {url} failed: {e}")
            return None

    @staticmethod
    def put(api_url, session=requests, headers={}, data=None, json_data=None):
        """Send a PUT request."""
        url = f"{api_url}"
        Logger.log("PUT:", url)
        
        try:
            response = session.put(url, data=data, json=json_data, headers=headers)
            return APIUtil._handle_response(response)
        except requests.exceptions.RequestException as e:
            Logger.log(f"PUT request to {url} failed: {e}")
            return None

    @staticmethod
    def delete(api_url, session=requests, headers={}):
        """Send a DELETE request."""
        
        url = f"{api_url}"
        Logger.log("DELETE:", url)
        try:
            response = session.delete(url, headers=headers)
            return APIUtil._handle_response(response)
        except requests.exceptions.RequestException as e:
            Logger.log(f"DELETE request to {url} failed: {e}")
            return None
