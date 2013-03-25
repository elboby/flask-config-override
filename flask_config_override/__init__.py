from flask import request
import logging

from .proxy_config import ProxyConfig
from .cookie_utils import cookie_to_json
from .blueprint import blueprint as config_override_bp


logger = logging.getLogger(__name__)


class ConfigOverride(object):
    """
    Flask extension used to control the config override mechanism.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._handle_config(app)

        if not app.config['CONFIG_OVERRIDE_COOKIE_ENABLED']:
            logger.debug("Config override disabled")
            return

        logger.debug("Attaching the proxy config...")
        app.config = ProxyConfig(app.config)

        logger.debug("Attaching the config override blueprint...")
        app.register_blueprint(config_override_bp,
                               url_prefix='/config_override')

        @app.before_request
        def override_config_from_cookie():
            """
            Load overriding config from cookie.
            """
            data = request.cookies.get(app.config['CONFIG_OVERRIDE_COOKIE_NAME'])
            logger.debug("Config override by cookie: %s" % data)

            try:
                if data:
                    app.config.set_overriden_configuration(cookie_to_json(data))
            except ValueError:
                logger.warning("Config override ABORTED as cookie is \
                               malformed: %s" % data)

    def _handle_config(self, app):
        """
        Setup default values if missing.
        """
        default = {'CONFIG_OVERRIDE_COOKIE_NAME': 'config_override_options',
                   'CONFIG_OVERRIDE_COOKIE_ENABLED': True,
                   'CONFIG_OVERRIDE_EXTENDABLE_VARS': [],
                   }
        default.update(app.config)
        app.config = default
