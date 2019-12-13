import json
import requests
from collections import OrderedDict

from django.db.models.loading import get_model
from django.conf import settings

from .constants import ALERT_ERROR, ALERT_WARNING
from .errors import (
    InvalidKeyError,
    InvalidAlertError,
    ConfigurationError,
)


def get_healthcheck_config(key):
    """
    Gets the configuration of the health check from external manifest file

    :param key: string
    :return: dict
    """
    # get the config from the external manifest file
    url = settings.DATA_SNIFFER_MANIFEST_FILE
    manifest_file = requests.get(url)
    if manifest_file.status_code == 200:
        HEALTH_CHECKS = json.loads(manifest_file.content)
    else:
        HEALTH_CHECKS = {}

    if key not in HEALTH_CHECKS:
        raise InvalidKeyError('Missing %s in health check manifest' % key)

    return HEALTH_CHECKS[key]


def get_healthcheck_status(key, refresh=False):
    """
    Gets the health check status. returns list of all assessed objects,
    enriched with data on each object's alerts + warnings

    :param key: string
    :param refresh: bool (clears cache)
    :return: SortedDict (of all objects, by ID), like
        {
            1L: {
                'id': 1L
                'object': <OrgPosition: Cat Wrestler>,
                'has_alert': False,
                'has_warning': True,
                'alerts': [],
                'warnings': ['Position is cat related'],
            }
        }
    """
    # TODO: get from cache if it's not expired

    config = get_healthcheck_config(key)

    # get the model
    if "model" not in config or not config["model"]:
        raise ConfigurationError("manifest file missing model for key '%s'" % key)
    model_app = config["model"].split(".")[0]
    model_name = config["model"].split(".")[1]
    model = get_model(model_app, model_name)

    # get the queryset
    queryset = model.objects.all()
    display_field = "id"
    extra_display_fields = []
    if "queryset" in config:
        if "filters" in config["queryset"] and config["queryset"]["filters"]:
            queryset = queryset.filter(**config["queryset"]["filters"])

        if "excludes" in config["queryset"] and config["queryset"]["excludes"]:
            queryset = queryset.exclude(**config["queryset"]["excludes"])

        if "ordering" in config["queryset"] and config["queryset"]["ordering"]:
            queryset = queryset.order_by(config["queryset"]["ordering"])

        if "display_field" in config["queryset"] and config["queryset"]["display_field"]:
            display_field = config["queryset"]["display_field"]

        if "extra_display_fields" in config["queryset"]:
            extra_display_fields = config["queryset"]["extra_display_fields"]

        queryset = queryset.distinct()

    # get any additional data
    additional_values = queryset.values_list('id', *extra_display_fields)
    additional_values = {v[0]:v[1:] for v in additional_values}

    # populate the ordered dict of items
    status = OrderedDict()
    for obj in queryset:
        status[obj.id] = {
            "id": obj.id,
            "display_name": getattr(obj, display_field),
            "additional_values": additional_values[obj.id],
            "has_warning": False,
            "has_alert": False,
            "warnings": [],
            "alerts": []
        }

    # get the objects that have warnings/alerts
    for alert in config["alerts"]:
        # ensure has valid name + message
        if "name" not in alert or not alert["name"]:
            raise InvalidAlertError("Alert without name")
        if "message" not in alert or not alert["message"]:
            raise InvalidAlertError("'%s' alert has no message" % alert["name"])

        # ensure has valid queryset
        if "queryset" not in alert or (not alert["queryset"]["filters"] and not alert["queryset"]["excludes"]):  # noqa
            raise InvalidAlertError(
                "'%s' alert has no queryset" % alert["name"])

        alerted_objects = queryset
        if "filters" in alert["queryset"] and alert["queryset"]["filters"]:
            alerted_objects = alerted_objects.filter(
                **alert["queryset"]["filters"])
        if "excludes" in alert["queryset"] and alert["queryset"]["excludes"]:
            alerted_objects = alerted_objects.exclude(
                **alert["queryset"]["excludes"])

        # update the status for the alerted on object
        alerting_ids = alerted_objects.values_list('id', flat=True)
        for alerting_id in alerting_ids:
            if alert["level"] == ALERT_WARNING:
                status[alerting_id]["has_warning"] = True
                status[alerting_id]["warnings"].append(alert["message"])
            elif alert["level"] == ALERT_ERROR:
                status[alerting_id]["has_alert"] = True
                status[alerting_id]["alerts"].append(alert["message"])
            else:
                raise InvalidAlertError(
                    "'%s' alert has invalid level" % alert["name"])

    return status

