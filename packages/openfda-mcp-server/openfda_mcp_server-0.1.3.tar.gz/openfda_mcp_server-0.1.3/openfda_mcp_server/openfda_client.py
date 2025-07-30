import requests


class OpenFDAClient:
    """Client for interacting with the OpenFDA API to fetch drug safety data."""

    BASE_URL = "https://api.fda.gov"

    def __init__(self):
        pass

    def search(self, query: str, category="drug", endpoint="event", limit: int = 5):
        """Search for drug events using the OpenFDA API."""
        url = f"{self.BASE_URL}/{category}/{endpoint}.json"
        params = {"search": query, "limit": limit}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
