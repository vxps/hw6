import requests
from typing import Optional, Dict


class ExchangeRateClient:

    API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    DEFAULT_TIMEOUT = 10

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout

    def get_rates(self) -> Optional[Dict[str, float]]:
        try:
            response = requests.get(self.API_URL, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get('rates')
        except (requests.RequestException, ValueError) as e:
            return None