# coding: utf-8
"""
    vestlus is a django app with support for private and public channels.
"""
from __future__ import unicode_literals
from .requires import REQUIRED_APPS

__version__ = "0.1.4"
__license__ = 'BSD 3-Clause'
__copyright__ = 'Copyright 2020 Lehvitus ÖU'

VERSION = __version__

default_app_config = 'vestlus.apps.VestlusConfig'
