"""
Abstract class to handle alert tracker
"""

import json
import os
from abc import ABC, abstractmethod
from typing import TypeVar, Union

import requests as rq
from loguru import logger
from twilio.rest import Client

T = TypeVar("T", bound=Union[list, dict])


class AlertTracker(ABC):
    """
    Abstract class to handle alert tracker
    """

    def __init__(self, redis_client, whatsapp_config: dict, time_window: int = 300, alert_threshold: int = 5):
        """
        Constructor for the class

        :param redis_client: Redis client
        :param whatsapp_config: Whatsapp configuration
        :param time_window: Time window in seconds
        :param alert_threshold: Alert threshold
        """
        self.redis_client = redis_client
        self.whatsapp_config = whatsapp_config
        self.time_window = time_window
        self.alert_threshold = alert_threshold
        self._token = None

    @abstractmethod
    def process_alert(self, data: T):  # type: ignore
        """
        Process the alert
        """

    def send_whatsapp_notification(self, message_variables: dict, recipients: list):
        """
        Send a whatsapp notification
        """
        if not bool(os.getenv("SEND_WHATSAPP", "False") == "True"):
            logger.info("WhatsApp notifications are disabled")
            return False

        if not recipients:
            logger.warning("No recipients provided for WhatsApp notification")
            return False

        twilio_client = Client(self.whatsapp_config["twilio_account_sid"], self.whatsapp_config["twilio_auth_token"])
        for recipient in recipients:
            message_sent = twilio_client.messages.create(
                from_=self.whatsapp_config["twilio_phone_number"],
                content_sid=self.whatsapp_config["twilio_template_sid"],
                content_variables=json.dumps(message_variables),
                to=recipient,
            )
            logger.info(f"WhatsApp notification sent to {recipient} message: {message_sent.body}")  # type: ignore
        return True

    @abstractmethod
    def send_email_notification(self, message: str):
        """
        Send an email notification
        """

    def get_address_from_coordinates(self, latitude: float, longitude: float) -> str:
        """
        Get the address from coordinates using the free Nominatim API.

        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate

        Returns:
            str: Formatted address or empty string if error occurs
        """
        nominatim_url = "https://nominatim.openstreetmap.org/reverse"
        headers_list = [
            {"User-Agent": "Tako/1.0 (meliusid@meliusid.com)"},
            {"User-Agent": "Tako/2.0 (melius@meliusid.com)"},
        ]

        params = {"lat": latitude, "lon": longitude, "format": "json", "addressdetails": 1, "accept-language": "es"}

        for headers in headers_list:
            try:
                response = rq.get(nominatim_url, params=params, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    address = data.get("address", {})

                    components = {
                        "street": address.get("road", ""),
                        "neighborhood": address.get("neighbourhood", ""),
                        "suburb": address.get("suburb", ""),
                    }

                    if not any(components.values()):
                        return "Dirección no disponible"

                    return f"{components['street']}, Barrio {components['neighborhood']} {components['suburb']}"

            except Exception as e:  # noqa: BLE001
                logger.error("Error getting address from coordinates: %s", str(e))

        return ""

    def login_tako(self, url_login: str) -> str:
        """
        Login in the platform
        """
        payload_for_login = {"username": os.getenv("USERNAME_CCZ_LOGIN"), "password": os.getenv("PASSWORD_CCZ_LOGIN")}
        headers_for_login = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = rq.request("POST", url_login, headers=headers_for_login, data=payload_for_login, timeout=20)
            self._token = response.json()["access_token"]
            return self._token
        except KeyError:
            return ""

    def save_to_postgres(self, url: str, login_url, data: dict, token: None):
        """
        Save the alert to postgres
        """
        try:
            if not token:
                if not self._token:
                    self._token = self.login_tako(url_login=login_url)

                if self._token:
                    token = self._token  # type: ignore
                else:
                    logger.error("Could not obtain token for Postgres saving.")
                    return

            response = rq.post(
                url,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=10,
            )

            # Esto por si el token expira, volverlo a obtener nuevamente
            if response.status_code == 401:
                logger.info("Token expired, refreshing token...")
                self._token = self.login_tako(url_login=login_url)
                if not self._token:
                    logger.error("Could not obtain token for Postgres saving.")
                    return

                response = rq.post(
                    url,
                    headers={"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"},
                    data=json.dumps(data),
                    timeout=10,
                )

            response.raise_for_status()
        except rq.exceptions.Timeout:
            logger.error("Timeout error")
            return
        except rq.exceptions.ConnectionError:
            logger.error("Connection error")
            return
        except rq.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return
        except rq.exceptions.RequestException as e:
            logger.error(f"Request exception occurred: {e}")
            return
