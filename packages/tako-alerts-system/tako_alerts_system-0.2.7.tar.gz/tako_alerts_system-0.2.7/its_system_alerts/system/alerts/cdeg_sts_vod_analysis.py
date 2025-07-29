"""
Class to handle alert related to EV11 - ITS
Request from CDEG to STS for Video-on-Demand Access
'Petición desde el CDEG al STS para el acceso de video por demanda.'
"""

import datetime
import os
import time

import pytz
import redis
from loguru import logger

from its_system_alerts.system.alerts.alert_tracker import AlertTracker

EVENT_CODE = "EV11"


class CDEGSTSVoDRequestAnalyzer(AlertTracker):
    """
    Class to handle alert related to EV11
    """

    def __init__(
        self, redis_client: redis.Redis, whatsapp_config: dict, time_window: int = 300, alert_threshold: int = 5
    ):
        """
        Initialize the code
        """
        super().__init__(redis_client, whatsapp_config, time_window, alert_threshold)
        self._token_tako = None

    def _rule_activation(self, event_code: str) -> bool:
        """
        Check if the event code is EV11
        """
        return event_code == EVENT_CODE

    def send_email_notification(self, message: str):
        raise NotImplementedError

    def _get_tako_token(self, login_url: str):
        """
        Get token from local storage
        """
        if self._token_tako is None:
            self._token_tako = self.login_tako(url_login=login_url)
        return self._token_tako

    def save_alert(self, data, alert_count, alert_type_code, address):
        """
        Save alert into the system
        """
        company_id = data.get("company_id")
        vehicle_id = data.get("idVehiculo")
        timestamp = data.get("fechaHoraLecturaDato")
        route = data.get("idRuta")
        latitud = data.get("localizacionVehiculo", {}).get("latitud")
        longitud = data.get("localizacionVehiculo", {}).get("longitud")

        dt = datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S.%f")
        formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")

        alert = {
            "vehicle": vehicle_id,
            "longitud": str(longitud),
            "latitud": str(latitud),
            "last_reported_time": formatted_timestamp,
            "total_events": alert_count,
            "id_alert_type": alert_type_code,
            "send_whatsapp": False,
            "send_email": False,
            "company_id": company_id,
            "reported_its_route": route,
            "address": address,
        }

        url_post = os.getenv("URL_POST_ALERT", "")
        url_login = os.getenv("URL_LOGIN_TAKO", "")

        self.save_to_postgres(url=url_post, login_url=url_login, data=alert, token=self._token_tako)  # type: ignore

    def process_alert(self, data: dict):
        """
        Process the alert data
        """
        company_id = data.get("company_id")
        vehicle_id = data.get("idVehiculo")
        alert_code = data.get("codigoEvento", "-")
        timestamp = data.get("fechaHoraLecturaDato", None)
        latitud = data.get("localizacionVehiculo", {}).get("latitud")
        longitud = data.get("localizacionVehiculo", {}).get("longitud")

        if not all([company_id, vehicle_id, alert_code, timestamp]):
            return

        if not self._rule_activation(alert_code):
            return

        url_login = os.getenv("URL_LOGIN_TAKO", "")
        self._get_tako_token(login_url=url_login)

        redis_key = f"camera_access:{company_id}:{vehicle_id}:{alert_code}"
        current_time = time.time()

        local_tz = pytz.timezone("America/Bogota")
        dt = datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S.%f")
        dt_local = local_tz.localize(dt)
        dt_utc = dt_local.astimezone(pytz.utc)
        timestamp = dt_utc.timestamp()

        self.redis_client.zadd(redis_key, {timestamp: timestamp})
        self.redis_client.expire(redis_key, self.time_window * 5)
        self.redis_client.zremrangebyscore(redis_key, 0, current_time - self.time_window)
        alert_count = self.redis_client.zcard(redis_key)
        if alert_count >= self.alert_threshold:
            logger.info(
                f"Camera access alert triggered for company {company_id}, vehicle {vehicle_id}, alert code {alert_code}"
            )
            address = self.get_address_from_coordinates(latitud, longitud)
            self.save_alert(data=data, alert_count=alert_count, alert_type_code="7", address=address)
            self.redis_client.delete(redis_key)
