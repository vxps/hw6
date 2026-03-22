from abc import ABC, abstractmethod
from typing import Optional

class CurrencyConverter(ABC):
    @abstractmethod
    def convert(self, amount: float, target_currency: str) -> Optional[float]:
        pass

    @abstractmethod
    def get_rate(self, currency: str) -> Optional[float]:
        pass