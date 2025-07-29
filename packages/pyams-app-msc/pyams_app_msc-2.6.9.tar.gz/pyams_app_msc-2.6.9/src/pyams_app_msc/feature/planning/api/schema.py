# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from colander import Boolean, Integer, MappingSchema, SchemaNode, SequenceSchema, String, drop

from pyams_app_msc.feature.booking.api.schema import BookingList
from pyams_utils.rest import BaseResponseSchema


__docformat__ = 'restructuredtext'


#
# Planning API schemas
#

class PlanningSessionInfo(MappingSchema):
    """Planning session info"""
    id = SchemaNode(String(),
                    description="Session ID")
    title = SchemaNode(String(),
                       description="Session title")
    start = SchemaNode(String(),
                          description="Session start date")
    end = SchemaNode(String(),
                     description="Session end date")
    theater = SchemaNode(String(),
                         description="Theater name")
    room = SchemaNode(String(),
                      description="Room name")
    capacity = SchemaNode(Integer(),
                          description="Room capacity")
    temporary = SchemaNode(Boolean(),
                           description="Temporary session flag")
    bookable = SchemaNode(Boolean(),
                          description="Bookable session flag")
    public = SchemaNode(Boolean(),
                        description="Public session flag")
    notepad = SchemaNode(String(),
                         description="Session notepad",
                         missing=drop)
    requested_seats = SchemaNode(Integer(),
                                 description="Requested seats",
                                 missing=drop)
    confirmed_seats = SchemaNode(Integer(),
                                 description="Confirmed seats",
                                 missing=drop)
    can_update = SchemaNode(Boolean(),
                            description="User update permission",
                            missing=drop)
    
    
class PlanningSessionsList(SequenceSchema):
    """Planning sessions list"""
    session = PlanningSessionInfo()
    
    
class PlanningGetterResults(BaseResponseSchema):
    """Planning getter result"""
    results = PlanningSessionsList(description="Planning sessions list",
                                   missing=drop)
    
    
class PlanningGetterResponse(MappingSchema):
    """Planning getter response schema"""
    body = PlanningGetterResults()


#
# Session API schemas
#

class SessionInfo(PlanningSessionInfo):
    """Session info"""
    bookings = BookingList()
    
    
class SessionResult(BaseResponseSchema):
    """Session result"""
    session = SessionInfo(description="Session info",
                          missing=drop)
    
    
class SessionGetterResponse(MappingSchema):
    """Session getter response schema"""
    body = SessionResult()
