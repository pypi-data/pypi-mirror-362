from ..base_type import base_type
from typing import Optional

@base_type
class BusinessOpeningHoursInterval:
    '''
    Describes an interval of time during which a business is open.
    '''

    closing_minute: int
    '''
    The minute's sequence number in a week, starting on Monday, marking the end of the time interval during which the business is open; 0 - 8 * 24 * 60
    '''

    opening_minute: int
    '''
    The minute's sequence number in a week, starting on Monday, marking the start of the time interval during which the business is open; 0 - 7 * 24 * 60
    '''

