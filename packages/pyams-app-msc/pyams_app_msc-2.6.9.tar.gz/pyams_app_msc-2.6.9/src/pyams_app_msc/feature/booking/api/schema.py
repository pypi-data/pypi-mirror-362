# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

from colander import Boolean, Integer, MappingSchema, OneOf, SchemaNode, SequenceSchema, String, drop

from pyams_app_msc.feature.booking import BOOKING_STATUS
from pyams_utils.rest import BaseResponseSchema

__docformat__ = 'restructuredtext'


class BookingSearchQuery(MappingSchema):
    """Booking search query"""
    with_session_info = SchemaNode(Boolean(),
                                   description="Include session information",
                                   missing=False)


class BookingSearchRequest(MappingSchema):
    """Booking information request"""
    querystring = BookingSearchQuery()


class BookingInfo(MappingSchema):
    """Booking info"""
    id = SchemaNode(String(),
                    description="Booking ID")
    session_id = SchemaNode(String(),
                            description="Booking session ID")
    activity = SchemaNode(String(),
                          description="Booking activity name",
                          missing=drop)
    recipient = SchemaNode(String(),
                           description="Booking recipient name")
    establishment = SchemaNode(String(),
                               description="Booking establishment name")
    status = SchemaNode(String(),
                        description="Booking status")
    nb_participants = SchemaNode(Integer(),
                                 description="Booking participants count")
    participants_age = SchemaNode(String(),
                                  description="Booking participants age")
    nb_accompanists = SchemaNode(Integer(),
                                 description="Booking accompanists count")
    accompanying_ratio = SchemaNode(Integer(),
                                    description="Accompanying ratio defines the number of participants for "
                                                "which an accompanying person will have free access")
    nb_free_accompanists = SchemaNode(Integer(),
                                      description="Booking free accompanists count")
    nb_groups = SchemaNode(Integer(),
                           description="Booking groups count")
    price = SchemaNode(String(),
                       description="Booking price")
    cultural_pass = SchemaNode(Boolean(),
                               description="Booking cultural pass marker")
    comments = SchemaNode(String(),
                          description="Booking comments",
                          missing=drop)
    notepad = SchemaNode(String(),
                         description="Booking notepad",
                         missing=drop)
    can_update = SchemaNode(Boolean(),
                            description="Booking update permission flag",
                            missing=False)


class BookingList(SequenceSchema):
    """Booking list"""
    booking = BookingInfo()


class BookingSearchResult(BaseResponseSchema):
    """Booking search result"""
    results = BookingList(description="Bookings list",
                          missing=drop)

    
class BookingSearchResponse(MappingSchema):
    """Booking search response"""
    body = BookingSearchResult()
    

class BookingInfoQuery(MappingSchema):
    """Booking information query"""
    with_session_info = SchemaNode(Boolean(),
                                   description="Include session information",
                                   missing=False)
    
    
class BookingInfoRequest(MappingSchema):
    """Booking information request"""
    querystring = BookingInfoQuery()
    
    
class FullBookingInfo(BookingInfo):
    """Full booking info"""


class FullBookingInfoResult(BaseResponseSchema):
    """Full booking info result"""
    booking = FullBookingInfo(description="Full booking info",
                                missing=drop)
    
    
class FullBookingInfoResponse(MappingSchema):
    """Full booking info response"""
    body = FullBookingInfoResult()


class PriceItem(MappingSchema):
    """Price item"""
    id = SchemaNode(String(),
                    description="Price ID")
    name = SchemaNode(String(),
                      description="Price name")
    
    
class PriceList(SequenceSchema):
    """Price list"""
    price = PriceItem()
    

class CommentsList(SequenceSchema):
    """Comments list"""
    comment = SchemaNode(String(),
                         description="Comment")

    
class BookingValidationInfo(FullBookingInfo):
    """Booking validation info"""
    price = SchemaNode(String(),
                       description="Booking price",
                       missing=drop)
    available_prices = PriceList(description="Available prices",
                                 missing=drop)
    notify_subject = SchemaNode(String(),
                                description="Notification email subject",
                                missing=drop)
    notify_message = SchemaNode(String(),
                                description="Notification email message",
                                missing=drop)
    can_send_reminder = SchemaNode(Boolean(),
                                   description="Boolean flag used to specify if a reminder "
                                               "can be sentto recipient")
    reminder_subject = SchemaNode(String(),
                                  description="Reminder email subject",
                                  missing=drop)
    reminder_message = SchemaNode(String(),
                                  description="Reminder email message",
                                  missing=drop)
    notepads = CommentsList(desription="Notepads",
                            missing=drop)
    
    
class BookingValidationRequest(BookingInfoRequest):
    """Booking validation request"""

    
class BookingValidationGetterResult(BaseResponseSchema):
    """Booking validation getter result"""
    booking = BookingValidationInfo()
    
    
class BookingValidationGetterResponse(MappingSchema):
    """Booking validation getter response"""
    body = BookingValidationGetterResult()
    
    
class BookingValidationPostInfo(MappingSchema):
    """Booking validation post info"""
    status = SchemaNode(String(),
                        description="Booking status",
                        validator=OneOf((
                            BOOKING_STATUS.OPTION.value,
                            BOOKING_STATUS.ACCEPTED.value
                        )))
    price = SchemaNode(String(),
                       description="Selected booking price")
    accompanying_ratio = SchemaNode(Integer(),
                                    description="Accompanying ratio defines the number of participants for "
                                                "which an accompanying person will have free access",
                                    missing=0)
    notify_recipient = SchemaNode(Boolean(),
                                  description="Recipient notification flag",
                                  missing=False)
    notify_subject = SchemaNode(String(),
                                description="Recipient notification subject",
                                missing=drop)
    notify_message = SchemaNode(String(),
                                description="Recipient notification message",
                                missing=drop)
    include_quotation = SchemaNode(Boolean(),
                                   description="Include quotation flag",
                                   missing=False)
    quotation_message = SchemaNode(String(),
                                   description="Message added to quotation",
                                   missing=drop)
    send_reminder = SchemaNode(Boolean(),
                               description="Reminder notification flag",
                               missing=False)
    reminder_subject = SchemaNode(String(),
                                  description="Reminder subject",
                                  missing=drop)
    reminder_message = SchemaNode(String(),
                                  description="Reminder message",
                                  missing=drop)
    notepad = SchemaNode(String(),
                         description="Booking notepad",
                         missing=drop)
    
    
class BookingValidationPostRequest(MappingSchema):
    """Booking validation post request"""
    body = BookingValidationPostInfo()
    
    
class BookingValidationPostResult(BaseResponseSchema):
    """Booking validation post result"""
    
    
class BookingValidationPostResponse(MappingSchema):
    """Booking validation post response"""
    body = BookingValidationPostResult()
    