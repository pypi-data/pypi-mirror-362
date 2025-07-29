"""
This module defines the Application configuration attributes.
"""

# pylint: disable=no-self-argument
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Dict, Optional

from pydantic import Field, validator

# Internal libraries
from core_common_configuration.base_conf_env import BaseConfEnv

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["AppConf", "app_conf_factory"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                  APP Configuration                                                   #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class AppConf(BaseConfEnv):
    """This class contains the configuration attributes of the application.

    The attributes of this class are updated with the values of the environment variables.

    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    app_env: Optional[str] = Field(default=None, description="Name of the configured deployment environment")
    app_group: Optional[str] = Field(default=None, description="Name of the group to which the application belongs.")
    app_name: str = Field(..., description="API application name")
    app_version: str = Field(..., description="API application version")
    app_id: Optional[str] = Field(default=None, description="Name that identifies the deployed API application")

    @validator("app_env")
    def no_hyphen(cls, value: str):
        """
        We want to remove any hyphen if value is not the empty string.
        """
        return value[1:] if value and value.startswith("-") else value


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                              APP Configuration Factory                                               #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def app_conf_factory(
    _env_file: Optional[str] = None, prefix: Optional[str] = None, defaults: Optional[Dict] = None, **kwargs
) -> AppConf:
    """This is a factory generating a AppConf class specific to a service, loading every value from a generic .env file
    storing variables in uppercase with a service prefix.

        example .env:
           PREFIX_APP_ENV='DEV'
           PREFIX_APP_VERSION='1.0.0'
           ...

    Args:
        _env_file (str): Configuration file of the environment variables from where to load the values.
        prefix (str): Prefix that the class attributes must have in the environment variables.
        defaults (Optional:Dict): New values to override the default field values for the configuration model.
        kwargs (**Dict): Arguments passed to the Settings class initializer.

    Returns:
        conf (AppConf): Object of the required configuration class

    """
    return AppConf.with_defaults(env_file=_env_file, env_prefix=prefix, defaults=defaults, **kwargs)
