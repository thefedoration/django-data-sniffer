django-data-sniffer
================

**django-data-sniffer** provides a set of tools to inspect the data in your
service for misconfigurations

Features
========

- Configurable warning/alert queries on any database table in your django app
- A view to see all misconfigured objects in your table
- Ability to modify your queries via an externally hosted manifest file so
that adding a new health check doesn't require a deployment

Coming Soon
========

- Filters & grouping
- Search
- Pagination
- Get manifest file from util method instead of URL
- JSON API response
- Notifications

Setup
=============

#### Installation

    pip install django_data_sniffer

#### Add to settings.py
    
    INSTALLED_APPS = (
      ...
      'data_sniffer
      ...
    )
    
    DATA_SNIFFER_ENABLED = True
    DATA_SNIFFER_MANIFEST_FILE = 'https://path/to/your/manifest/file.json'  # noqa

#### Configuring the manifest file
Here's an example manifest file

    {
        "clients": {
            "name": "Active clients healthcheck",
            "model": "yourapp.Client",
            "queryset": {
                "filters": {
                    "status": "active"
                },
                "excludes": null,
                "ordering": null,
                "display_field": "name",
                "extra_display_fields": ["id", "membership_type"]
            },
            "alerts": [
                {
                    "level": "WARNING",
                    "name": "Missing billing",
                    "queryset": {
                        "filters": {
                            "billing_configured": false
                        }
                    },
                    "message": "Client does not have billing set up"
                },
                {
                    "level": "ERROR",
                    "name": "Missing billing and getting premium features",
                    "queryset": {
                        "filters": {
                            "billing_configured": false,
                            "premium_features_enabled": true
                        },
                        "excludes": {
                            "is_demo": true
                        }
                    },
                    "message": "Client has invalid feature set"
                }
            ]
        }
    }

    
    