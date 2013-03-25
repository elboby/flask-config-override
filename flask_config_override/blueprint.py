from flask import Blueprint, make_response, redirect, current_app, request
import logging

from .proxy_config import NonOverridableError
from .cookie_utils import json_to_cookie


blueprint = Blueprint('config_override_bp', __name__)

logger = logging.getLogger(__name__)


@blueprint.route("/")
def show_config():
    """
    Display the content of the overridden configuration.
    """
    return str(current_app.config.get_overridden_config())


@blueprint.route("/update/<config_key>/<config_value>/")
def update_config(config_key, config_value):
    """
    Update overridden data. Redirect to homepage if flag true.
    """
    try:
        current_app.config.update_overridden_config(config_key, config_value)
    except NonOverridableError, e:
        return ("ERROR trying to override a params which "
                "is not allowed: " + e.message)

    override_data = current_app.config.get_overridden_config()

    message = "Overridden config updated to: " + str(override_data)
    logger.debug(message)

    if request.args.get('redirect', None):
        response = make_response(redirect('/', 301))
    else:
        response = make_response(message)

    response.set_cookie(current_app.config['CONFIG_OVERRIDE_COOKIE_NAME'],
                        json_to_cookie(override_data))

    return response


@blueprint.route("/reset/")
def reset_config():
    """
    Reset the configuration to default values by deleting the cookie.
    """
    response = make_response("Overridden config reset")
    response.delete_cookie(current_app.config['CONFIG_OVERRIDE_COOKIE_NAME'])

    return response
