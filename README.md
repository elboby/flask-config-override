flask-config-override
=====================

[![Build Status](https://travis-ci.org/elboby/flask-config-override.png?branch=master)](https://travis-ci.org/elboby/flask-config-override)

This extension allows to change the configuration of a Flask application at runtime. This behavior is controlled by cookie and therefore is contained to the session of an unique user; configuration changes are not affecting other users.

A common usage is to quickly change options in staging environment without having to redeploy configuration changes. For example, we use it for an external API location or a feature switch like using minified Javascript files or not.

The configuration options able to be overridden are limited and configurable as well (using CONFIG_OVERRIDE_EXTENDABLE_VARS). This option can NOT be overridden for security reason.

The idea is to replace the configuration object of a Flask application by a proxy object, whom behavior can be controlled/changed upon request while exposing the same interface as a Flask configuration. The extension also provide a blueprint (default base url to /config_override/) to control the cookie via some simple HTTP calls; this is automatically attached to the application.

Installation
============
Via Pypi:

    pip install flask-config-override

Usage
=====
Once installed, first attach the extension to your Flask application:

    from flask import Flask
    from flask.ext.config_override import ConfigOverride

    app = Flask(__name__)
    app.config['FOO'] = 'bar'

    # Enable the override for the DEBUG option (default to false)
    app.config['CONFIG_OVERRIDE_EXTENDABLE_VARS'] = ['FOO']
    config_override = ConfigOverride(app)

    # configure your routes and what not...

Launch your app, then open your browser and go to this url to setup the FOO option to another value; here "toto":

    http://localhost:5000/config_override/update/FOO/toto/

Your session will now run with the settings FOO set to the new value. You can access it normally from `app.config['FOO']` within the context of a request.

To see the current changes, you can visit this url:

    http://localhost:5000/config_override/

And to remove the changes, you just need to clear your cookie or go there:

    http://localhost:5000/config_override/reset/


Tests
=====
* First install `nose` for test discovery: `pip install nose`
* Then run the tests within a virtual environment: `nosetests`


Contact
=======
Feel free to post issues, pull requests in github or contact me directly on twitter @el_boby.


Immediate TODOs
===============
* test for cookie_utils
* test for proxy_config (based on flask one)
* documentation API (sphinx)


TODO
====
* Override by Environment variables.
* Flask Debug Toolbar integration.