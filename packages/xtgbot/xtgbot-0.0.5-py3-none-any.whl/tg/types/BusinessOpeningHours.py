from .BusinessOpeningHoursInterval import BusinessOpeningHoursInterval
from ..base_type import base_type
from typing import Optional

@base_type
class BusinessOpeningHours:
    '''
    Describes the opening hours of a business.
    '''

    opening_hours: list[BusinessOpeningHoursInterval]
    '''
    List of time intervals describing business opening hours
    '''

    time_zone_name: str
    '''
    Unique name of the time zone for which the opening hours are defined
    '''

