from __future__ import absolute_import

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .errors import (
    InvalidKeyError, ConfigurationError, InvalidAlertError
)
from .utils import get_healthcheck_status, get_healthcheck_config

@staff_member_required
def data_sniffer_health_check(request, key):
    """
    Serves up default health check template
    """
    try:
        config = get_healthcheck_config(key)
    except InvalidKeyError:
        return redirect('/404/')

    try:
        status = get_healthcheck_status(key)
    except ConfigurationError:
        return render(request, 'data_sniffer/invalid.html', {
            'error': "Misconfigured health check",
        }, status=400)
    except InvalidAlertError:
        return render(request, 'data_sniffer/invalid.html', {
            'error': "Misconfigured health check alert",
        }, status=400)

    show_all = True if request.GET.get('all', False) else False
    if show_all:
        objects = [status[obj_id] for obj_id in status]
    else:
        objects = [status[obj_id] for obj_id in status if status[obj_id]['has_warning'] or status[obj_id]['has_alert']]  # noqa

    # put into groupings based on category, must be in "extra_display_fields"
    category_key = request.GET.get('category', None)
    categories = {}
    if category_key and "extra_display_fields" in config["queryset"]:
        index = config["queryset"]["extra_display_fields"].index(category_key)
        for object in objects:
            obj_category = object["additional_values"][index]
            if obj_category not in categories:
                categories[obj_category] = {
                    "value": obj_category,
                    "objects": [],
                    "has_warning": False,
                    "has_alert": False
                }
            categories[obj_category]["objects"].append(object)
            if object["has_warning"]:
                categories[obj_category]["has_warning"] = True
            if object["has_alert"]:
                categories[obj_category]["has_alert"] = True

        # put into list. no particular order yet
        categories = [categories[i] for i in categories]

    return render(request, 'data_sniffer/status.html', {
        'key': key,
        'config': config,
        'objects': objects,
        'categories': categories,
        'show_all': show_all,
        'count_total': len(status),
        'count_warnings': len([o for o in objects if o['has_warning']]),
        'count_alerts': len([o for o in objects if o['has_alert']]),
    })
