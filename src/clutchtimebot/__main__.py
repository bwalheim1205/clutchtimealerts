from clutchtimebot.clutch_alerts import ClutchAlertsService
from clutchtimebot.notifications.groupme import GroupMeNotification

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose a notification type.")
    parser.add_argument(
        "--type",
        type=str,
        required=False,
        default="groupme",
        choices=["groupme"],
        help="The type of notifcations to use (Default: groupme).",
    )

    args = parser.parse_args()

    if args.type == "groupme":
        notification = GroupMeNotification()

    alert_service = ClutchAlertsService(notification=notification)
    alert_service.run()
