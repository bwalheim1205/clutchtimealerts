from clutchtimebot.clutch_alerts import ClutchAlertsService
from clutchtimebot.notifications.groupme import GroupMeNotification
from clutchtimebot.config_parser import ConfigParser
from clutchtimebot.notification_collector import NotificationCollector

import argparse
import os

if __name__ == "__main__":
    # Parse Arguments
    parser = argparse.ArgumentParser(description="Choose a notification type.")
    parser.add_argument(
        "-f" "--file",
        dest="file",
        default="config.yml",
        type=str,
        required=False,
        help="Path to the YAML config file",
    )
    args = parser.parse_args()

    # Collect Notification Classes
    collector = NotificationCollector()
    notifcation_dir = os.path.dirname(__file__) + "/notifications"
    collector.collect_notifications(notifcation_dir)

    # Parse Config
    parser = ConfigParser(
        args.file, collector.classname_dict, collector.common_name_dict
    )
    parser.parse_config()

    alert_service = ClutchAlertsService(
        notifications=parser.notifications,
        db_path=parser.db_file_path,
        db_table_name=parser.db_table_name,
    )
    alert_service.run()
