from flask import g, current_app
import logging

logger = logging.getLogger(__name__)


class NonOverridableError(Exception):
    """
    For attempt to override an non extendable config variable.
    """
    def __init__(self, arg):
        self.args = arg
        self.message = "Not allowed to override this config: " + arg


class ProxyConfig(object):
    """
    Proxy object for config, which will read from overridden data if needed.
    Will proxy all the methods calls as well.
    """
    __subject = None

    def __init__(self, subject):
        self.__subject = subject

    def __getattribute__(self, attr_name):
        try:
            # call on self
            retval = super(ProxyConfig, self).__getattribute__(attr_name)
        except AttributeError:
            # call on child object
            retval = self.__subject.__getattribute__(attr_name)

        return retval

    def __getitem__(self, name):
        if not self._is_internal(name) and self._is_overridden(name):
            return self._get_overridden_attribute(name)

        return self.__subject[name]

    def __setitem__(self, name, value):
        if self._is_internal(name):
            return object.__setitem__(self, name, value)

        self.__subject[name] = value

    def __getattr__(self, name):
        if not self._is_internal(name) and self._is_overridden(name):
            return self._get_overridden_attribute(name)

        return getattr(self.__subject, name)

    def __setattr__(self, name, value):
        if self._is_internal(name):
            return object.__setattr__(self, name, value)

        setattr(self.__subject, name, value)

    def _is_internal(self, name):
        """
        Check if the key is for internal attribute.
        """
        return name == '_ProxyConfig__subject'

    def _is_overridden(self, name):
        """
        Check that the key is actually overridden.
        """
        if self._may_be_overridden(name):
            return False

        if self._is_overridden_globally(name):
            return True

        return False

    def _may_be_overridden(self, name):
        """
        Check whether the given key is allowed to be overriden.
        """
        return (name == 'CONFIG_OVERRIDE_EXTENDABLE_VARS' and
                not name in self.__subject['CONFIG_OVERRIDE_EXTENDABLE_VARS'])

    def _is_overridden_globally(self, name):
        """
        Check whether the given key is already overridden globally.
        """
        return (hasattr(g, 'overridden_config') and
                name in g.overridden_config)

    def _get_overridden_attribute(self, name):
        """
        Retrieve the overridden value.
        """
        debug_message_template = "Using overridden value for: %s -> %s"
        debug_message = debug_message_template % (name,
                                                  g.overridden_config[name])
        logger.debug(debug_message)
        return g.overridden_config[name]

    def set_overriden_configuration(self, override_data):
        """
        Register a subset of configuration that will override the normal
        configuration.
        """
        logger.debug("registering config override %s" % override_data)
        g.overridden_config = override_data

    def get_overridden_config(self):
        """
        Return current overridden config.
        """
        if not hasattr(g, 'overridden_config'):
            return None

        return g.overridden_config

    def update_overridden_config(self, key, value):
        """
        Update a key value of the overridden config. Create if none.
        Check also if updatable.
        """
        if not key in current_app.config['CONFIG_OVERRIDE_EXTENDABLE_VARS']:
            raise NonOverridableError(key)

        if not hasattr(g, 'overridden_config'):
            g.overridden_config = {}

        g.overridden_config[key] = value
