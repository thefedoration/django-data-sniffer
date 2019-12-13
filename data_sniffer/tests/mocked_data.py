from ..constants import ALERT_WARNING, ALERT_ERROR, NOTIFICATION_EMAIL

HEALTH_CHECKS = {
    "positions": {
        "name": "Position healthcheck",
        "model": "organizations.OrgPosition",
        "queryset": {
            "filters": {
                "position__status": "ACT"
            },
            "excludes": None,
            "ordering": None,
            "display_field": "name",
            "extra_display_fields": ["organization__name", "project__name"]
        },
        "alerts": [
            {
                "level": ALERT_WARNING,
                "name": "cat check",
                "queryset": {
                    "filters": {
                        "name__contains": "Cat"
                    },
                    "excludes": None,
                },
                "message": "Position is cat related",
                "notification": {
                    "type": NOTIFICATION_EMAIL,
                    "email": "fedorgarin@pymetrics.com",
                    "url": "",
                }
            },
            {
                "level": ALERT_ERROR,
                "name": "flymetrics check",
                "queryset": {
                    "filters": {
                        "organization__name__contains": "flymetrics"
                    },
                    "excludes": None,
                },
                "message": "Flymetrics hasnt paid their bills",
            }
        ]
    }
}