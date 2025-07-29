#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

from collections import OrderedDict

from enum import Enum
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import contains
from zope.container.interfaces import IContainer
from zope.schema import Bool, Choice, Datetime, Int, List, Text, TextLine, Timedelta
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_app_msc.shared.theater.interfaces.audience import AUDIENCES_VOCABULARY
from pyams_app_msc.shared.theater.interfaces.room import ROOMS_SEATS_VOCABULARY

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class VERSION_INFO(Enum):
    """Version information"""
    OV = 'ov'
    OVWS = 'ovws'
    TF = 'tf'


VERSION_INFO_LABEL = OrderedDict((
    (VERSION_INFO.OV, _("Original version")),
    (VERSION_INFO.OVWS, _("Original version with subtitles")),
    (VERSION_INFO.TF, _("Translated version"))
))

VERSION_INFO_ABBR = {
    VERSION_INFO.OV: _("OV"),
    VERSION_INFO.OVWS: _("OVWS"),
    VERSION_INFO.TF: _("TV")
}


VERSION_INFO_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v.value, title=t)
    for v, t in VERSION_INFO_LABEL.items()
])


class ISession(IAttributeAnnotatable):
    """Session interface"""

    def get_target(self):
        """Planning target getter"""

    label = TextLine(title=_("Label"),
                     description=_("If no label is set, activity label will be used"),
                     required=False)

    def get_label(self):
        """Session label getter"""

    start_date = Datetime(title=_("Session start date"),
                          description=_("Start date and time of the session"),
                          required=True)

    duration = Timedelta(title=_("Duration"),
                         description=_("Session duration, given as time delta object"),
                         required=True)

    end_date = Datetime(title=_("Session end date"),
                        description=_("End date and time of the session"),
                        required=True)

    room = Choice(title=_("Session room"),
                  description=_("Theater room in which session is planned"),
                  vocabulary=ROOMS_SEATS_VOCABULARY,
                  required=True)

    def get_room(self):
        """Room getter"""

    capacity = Int(title=_("Session capacity"),
                   description=_("Number of places available for this session"),
                   required=False)

    version = Choice(title=_("Displayed version"),
                     vocabulary=VERSION_INFO_VOCABULARY,
                     required=False)

    audiences = List(title=_("Selected audiences"),
                     description=_("List of audiences selected for this session"),
                     value_type=Choice(vocabulary=AUDIENCES_VOCABULARY),
                     required=False)

    def get_contacts(self):
        """Iterator over audiences contacts"""

    temporary = Bool(title=_("Temporary session"),
                     description=_("If 'yes', this session is 'temporary' and not confirmed yet!"),
                     required=True,
                     default=False)

    bookable = Bool(title=_("Open for internal booking"),
                    description=_("Only internal bookable sessions are visible to operators for booking"),
                    required=True,
                    default=True)
    
    extern_bookable = Bool(title=_("Open for external booking"),
                           description=_("Only external bookable sessions are visible to public for booking"),
                           required=True,
                           default=False)

    public_session = Bool(title=_("Public session"),
                          description=_("If 'yes', this session is public and anybody can assist"),
                          required=True,
                          default=False)

    comments = Text(title=_("Movie theater comments"),
                    description=_("These comments will be displayed to the users on booking form"),
                    required=False)

    notepad = Text(title=_("Notepad"),
                   description=_("These comments are for internal use only"),
                   required=False)


PLANNING_ANNOTATION_KEY = 'msc.planning'


class IPlanning(IContainer):
    """Planning container interface"""

    contains(ISession)

    def add_session(self, session):
        """Add new session to container"""


class IPlanningTarget(IAttributeAnnotatable):
    """Planning target marker interface"""


class IWfPlanningTarget(IPlanningTarget):
    """Workflow managed planning target"""
