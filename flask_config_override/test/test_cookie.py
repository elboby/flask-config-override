import unittest
from flask import Flask
from flask.ext.config_override import ConfigOverride
from flask.ext.config_override.cookie_utils import json_to_cookie


CURRENT_CONFIG = {
    'API_DOMAIN': "api.example.com",
    'COUNTRY': 'Australia',

    'CONFIG_OVERRIDE_COOKIE_NAME':  'config_override_options',
    'CONFIG_OVERRIDE_COOKIE_ENABLED':  True,
    'CONFIG_OVERRIDE_EXTENDABLE_VARS': ['API_DOMAIN', 'DEBUG'],
}


class CookieTestCase(unittest.TestCase):
    def setUp(self):
        # Create an Flask application instance for testing.
        app = Flask(__name__)
        app.secret_key = 'testkey'
        app.testing = True
        app.config.update(CURRENT_CONFIG)

        # Attach routes for testing values in the app config.
        @app.route('/test_default_config/<config_key>/')
        def test_default_config(config_key):
            self.assertEqual(CURRENT_CONFIG[config_key],
                             app.config[config_key])
            return ''

        @app.route('/test_overridden_config/<config_key>/<value_expected>/')
        def test_overridden_config(config_key, value_expected):
            self.assertEqual(value_expected,
                             app.config[config_key])
            return ''

        # Attach the ConfigOverride to the created app
        ConfigOverride(app)

        # instance available for testing
        self.app = app

    def tearDown(self):
        """ Common teardown for all the tests goes here """
        self.app = None

    def test_configuration_default(self):
        c = self.app.test_client()
        c.get('/test_default_config/API_DOMAIN/')
        c.get('/test_default_config/COUNTRY/')

    def test_configuration_override_is_available(self):
        c = self.app.test_client()
        rv = c.get('/config_override/')
        self.assertEquals(rv.status_code, 200)

    def test_configuration_overridden_more(self):
        c = self.app.test_client()
        c.get('/test_default_config/API_DOMAIN/')
        c.set_cookie('localhost',
                     CURRENT_CONFIG['CONFIG_OVERRIDE_COOKIE_NAME'],
                     value=json_to_cookie({'API_DOMAIN': 'bar'}))
        c.get('/test_overridden_config/API_DOMAIN/bar/')

    def test_configuration_overridden_blueprint(self):
        c = self.app.test_client()
        c.get('/test_default_config/API_DOMAIN/')
        c.get('/config_override/update/API_DOMAIN/bar/')
        c.get('/test_overridden_config/API_DOMAIN/bar/')
        c.get('/config_override/reset/')
        c.get('/test_default_config/API_DOMAIN/')

    def test_configuration_overridden_redirect(self):
        c = self.app.test_client()
        c.get('/test_default_config/API_DOMAIN/')
        rv = c.get('/config_override/update/API_DOMAIN/bar/?redirect=True')
        self.assertEquals(rv.status_code, 301)
        self.assertEquals('http://localhost/', rv.headers['Location'])
        c.get('/test_overridden_config/API_DOMAIN/bar/')

    def test_configuration_overridden_security(self):
        c = self.app.test_client()
        c.get('/test_default_config/COUNTRY/')
        c.get('/config_override/update/COUNTRY/France/')
        c.get('/test_overridden_config/COUNTRY/Australia/')


class CookieDisabledTestCase(unittest.TestCase):
    def setUp(self):
        # Create an Flask application instance for testing.
        app = Flask(__name__)
        app.config.update(CURRENT_CONFIG)
        
        # Disable the override via configuration
        app.config['CONFIG_OVERRIDE_COOKIE_ENABLED'] = False

        # Attach the ConfigOverride to the created app
        ConfigOverride(app)

        # instance available for testing
        self.app = app

    def test_configuration_override_is_gone(self):
        c = self.app.test_client()
        rv = c.get('/config_override/')
        self.assertEquals(rv.status_code, 404)
