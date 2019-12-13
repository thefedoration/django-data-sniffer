import mock

from django.test import SimpleTestCase

from .mocked_data import HEALTH_CHECKS
from ..constants import ALERT_WARNING
from ..utils import get_healthcheck_config, get_healthcheck_status
from ..errors import ConfigurationError, InvalidAlertError


class TestHealthcheckUtils(SimpleTestCase):
    def test_get_healthcheck_config(self):
        # test lookup method
        config = get_healthcheck_config("positions")
        self.assertEquals(config, HEALTH_CHECKS["positions"])

        # test exception
        with self.assertRaises(Exception):
            get_healthcheck_config("somethingrandom")

    def test_get_healthcheck_status(self):
        # just make sure we dont throw an exception
        get_healthcheck_status("positions")

        # TODO: test that the filtering works



class TestConfigurationsUtils(SimpleTestCase):
    """
    Tests for throwing configuration errors
    """

    @mock.patch("health_checks.utils.get_healthcheck_config",
                return_value=HEALTH_CHECKS["positions"])
    def test_valid_configuration(self, _):
        # make sure there are no exceptions thrown
        get_healthcheck_status("positions")

    @mock.patch("health_checks.utils.get_healthcheck_config", return_value={})
    def test_no_model(self, _):
        with self.assertRaises(ConfigurationError):
            get_healthcheck_status("test")

    @mock.patch("health_checks.utils.get_healthcheck_config", return_value={
        "name": "some name",
        "model": "organizations.OrgPosition",
        "alerts": [
            {}
        ]
    })
    def test_alert_missing_queryset(self, _):
        with self.assertRaises(InvalidAlertError):
            get_healthcheck_status("test")

    def test_alert_incorrect_level(self):
        pass