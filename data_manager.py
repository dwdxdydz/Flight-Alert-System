import requests

class DataManager:
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.bearer_token = f"Bearer {token}"
        self.header = {
            "Content-Type": "application//json",
            "Authorization": self.bearer_token
        }
        self.data = []

    def _make_request(self, method, url, json=None):
        """Helper method to make HTTP requests."""
        try:
            response = requests.request(method, url, headers=self.header, json=json)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_flight_data(self):
        """Retrieve flight data from the endpoint."""
        url = f"{self.endpoint}//prices"
        result = self._make_request("GET", url)
        if result:
            self.data = result.get('prices', [])
        return self.data

    def update_flight_data(self, row_id, payload):
        """Update flight data at the specified row_id."""
        url = f"{self.endpoint}//prices//{row_id}"
        body = {"price": payload}
        result = self._make_request("PUT", url, json=body)
        if result:
            print(result)
        return result

    def add_user(self, user):
        """Add a new user to the database."""
        url = f"{self.endpoint}//users"
        body = {
            "user": {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email
            }
        }
        result = self._make_request("POST", url, json=body)
        if result:
            print(result)
        return result

    def get_users(self):
        """Retrieve user data from the endpoint."""
        url = f"{self.endpoint}//users"
        result = self._make_request("GET", url)
        if result:
            self.data = result.get('users', [])
        return self.data
