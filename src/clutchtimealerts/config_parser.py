from clutchtimealerts.db_utils import TABLE_NAME
from clutchtimealerts.notifications.base import NotificationConfig
import yaml
import logging

logger = logging.getLogger("clutchtimealerts")

DEFAULT_NOTIFICATION_FORMAT = "Clutch Game\n{HOME_TEAM_TRI} {HOME_TEAM_SCORE} - {AWAY_TEAM_SCORE} {AWAY_TEAM_TRI}\n{NBA_COM_STREAM}"
DEFAULT_OT_FORMAT = "OT{OT_NUMBER} Alert\n{HOME_TEAM_TRI} {HOME_TEAM_SCORE} - {AWAY_TEAM_SCORE} {AWAY_TEAM_TRI}\n{NBA_COM_STREAM}"


class ConfigParser:
    def __init__(
        self,
        config_path: str = "config.yaml",
        classname_dict: dict = {},
        common_name_dict: dict = {},
    ) -> None:
        self.config_path = config_path
        self.classname_dict = classname_dict
        self.common_name_dict = common_name_dict

    def parse_config(self) -> None:
        # Parse YAML Config
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)

        # Parse database file path
        self.db_url = config.get("db_url", "sqlite:///clutchtime.db")

        # Parse Notifcation Format
        notification_format = config.get(
            "notification_format", DEFAULT_NOTIFICATION_FORMAT
        )
        ot_format = config.get("ot_format", DEFAULT_OT_FORMAT)

        notification_yaml = config.get("notifications", [])
        self.notification_configs = []
        for notify_config in notification_yaml:
            if "type" not in notify_config:
                raise ValueError("Notification type must be specified in config file")

            # Get YAML Config
            notifiction_type = notify_config["type"]
            class_config = notify_config["config"]

            # Check that notification type exists
            if notifiction_type in self.classname_dict:
                notification_class = self.classname_dict[notifiction_type]
            elif notifiction_type in self.common_name_dict:
                notification_class = self.common_name_dict[notifiction_type]
            else:
                logger.warning(
                    f"Unknown notification type: {notifiction_type} ... skipping"
                )
                continue

            # Instatiate Notification
            try:
                notification_instance = notification_class(**class_config)
            except Exception as e:
                logger.warning(
                    f"Failed to create notification of type {notifiction_type}: {e} ... skipping"
                )
                continue

            # Create notification config
            notification_config = NotificationConfig(
                notification=notification_instance,
                notification_format=notify_config.get(
                    "notification_format", notification_format
                ),
                ot_format=notify_config.get("ot_format", ot_format),
            )
            self.notification_configs.append(notification_config)

        if len(self.notification_configs) == 0:
            raise ValueError("No notifications found in config file")
