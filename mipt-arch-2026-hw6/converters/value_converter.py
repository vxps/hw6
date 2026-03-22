import logging
import time
from typing import Optional, Dict
from .currency_converter import CurrencyConverter
from .exchange_rate import ExchangeRateClient


class UsdConverter(CurrencyConverter):
    VALID_CURRENCIES = {'EUR', 'GBP', 'RUB', 'CNY'}
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self, client: Optional[ExchangeRateClient] = None):
        self.client = client or ExchangeRateClient()
        self.logger = self._setup_logger()
        self.rates: Optional[Dict[str, float]] = None
        self._load_rates()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
        return logger

    def _load_rates(self) -> bool:
        for attempt in range(self.MAX_RETRIES):
            self.rates = self.client.get_rates()
            if self.rates:
                self.logger.info("Курсы валют успешно загружены")
                return True

            self.logger.warning(f"Попытка {attempt + 1}/{self.MAX_RETRIES} не удалась")
            if attempt < self.MAX_RETRIES - 1:
                time.sleep(self.RETRY_DELAY)

        self.logger.error("Не удалось загрузить курсы валют")
        return False

    def convert(self, amount: float, target_currency: str) -> Optional[float]:
        if target_currency not in self.VALID_CURRENCIES:
            self.logger.error(f"Неподдерживаемая валюта: {target_currency}")
            return None

        if not self.rates:
            self.logger.error("Курсы валют не загружены")
            return None

        rate = self.rates.get(target_currency)
        if not rate:
            self.logger.error(f"Курс для {target_currency} не найден")
            return None

        return amount * rate

    def get_rate(self, currency: str) -> Optional[float]:
        if not self.rates:
            return None
        return self.rates.get(currency)